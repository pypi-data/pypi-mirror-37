#!python

import os
import sys
import re
import argparse
from datetime import datetime
import subprocess
import logging as l
from collections import Counter
if (sys.version_info > (3, 0)):
  import pathlib
else:
  import glob


# From https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch04s16.html
def splitall (path):
  allparts = []
  while 1:
    parts = os.path.split(path)
    if parts[0] == path:  # sentinel for absolute paths
      allparts.insert(0, parts[0])
      break
    elif parts[1] == path: # sentinel for relative paths
      allparts.insert(0, parts[1])
      break
    else:
      path = parts[0]
      allparts.insert(0, parts[1])
  return allparts


def read_rc (path):
  ''' read value in rc file '''
  with open(path) as f:
    rc = int(f.readline().strip())
  return rc


def ls_dtr_tasks (path):
  ''' quick and dirty listing of directories by mtime to get call order'''
  cmd = 'ls -dtr %s' % (path)
  return [ os.path.basename(p) for p in subprocess.check_output(cmd, shell=True, universal_newlines=True).split() ]


def calculate_timing (stdout_f):
  start = None
  end = None
  with open(stdout_f, 'r') as f:
    for line in f:
      m = re.match('Started at (.+)', line)
      if m:
        # %c is the "Locale appropriate date and time representation"
        # see https://docs.python.org/3/library/datetime.html#strftime-strptime-be
        start = datetime.strptime(m.group(1), '%c')
      m = re.match('Results reported on (.+)', line)
      if m:
        end = datetime.strptime(m.group(1), '%c')
        break

  if not start or not end:
    l.error('Could not parse start or end')
    sys.exit(1)

  td = end - start
  retval = {}
  retval['total_time'] = td
  retval['total_hours'] = td.total_seconds()/60/60
  retval['total_minutes'] = td.total_seconds()/60
  # Resolution is in seconds, so cast to int
  retval['total_seconds'] = int(td.total_seconds())
  return retval

script_path = os.path.abspath(__file__)
FORMAT = '[%(asctime)s] %(levelname)s %(message)s'
l.basicConfig(format=FORMAT, level=l.INFO)
l.debug('%s begin' % (script_path))

description = '''
Summarize results of a Cromwell run

Only useful for cromwell-executions containing a single workflow
with a single run

Supports one level of shards

Ordering of tasks is based on mtime of the directory


'''

epilog = '''
'''

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter):
  pass
parser = argparse.ArgumentParser(description=description, epilog=epilog,
    formatter_class=CustomFormatter)

parser.add_argument('executions_p', 
    help='Path to cromwell-executions directory')
parser.add_argument('-t', '--timings', action='store_true', 
    help='Report timings')

args = parser.parse_args()

l.debug('cromwell-executions path: %s' % (args.executions_p))

if not os.path.isdir(args.executions_p):
  l.error('Directory %s does not exist' % (args.executions_p))
  sys.exit(1)

# Find all rc files
if (sys.version_info > (3, 0)):
  rc_paths = pathlib.Path(args.executions_p).glob('**/rc')
else:
  rc_paths = []
  for root, dirs, files in os.walk(args.executions_p):
    for file in files:
      if os.path.basename(file) == 'rc':
        rc_paths.append(os.path.join(root, file))

tasks = {}
timings = {}
for rc_path in rc_paths:
  rc = read_rc(rc_path)
  if args.timings:
    stdout_f = os.path.join(os.path.dirname(rc_path), 'stdout')
    timing = calculate_timing(stdout_f)

  if rc != 0:
    l.warn('Non-zero rc %d: %s' % (rc, rc_path))

  rc_split = splitall(rc_path)
  if rc_split[-3][:5] == 'shard':
    shard = rc_split[-3]
    task = rc_split[-4]
    if not task in tasks:
      tasks[task] = {}
    tasks[task][int(shard[6:])] = rc
    if args.timings:
      if not task in timings:
        timings[task] = {}
      timings[task][int(shard[6:])] = timing['total_seconds']
  else:
    task = rc_split[-3]
    tasks[task] = read_rc(rc_path)
    if args.timings:
      timings[task] = timing['total_seconds']

ordered_tasks = ls_dtr_tasks('%s/*/*/*' % (args.executions_p))

for task_name in ordered_tasks:
  if not task_name in tasks:
    l.warn('No rc file(s) for task %s' % (task_name))
    continue
  output = [task_name]
  task = tasks[task_name]
  if isinstance(task, dict):
    counts = Counter(task.values())
    counts_list = []
    for k in sorted(counts.keys()):
      counts_list.append('%d: %d' % (k, counts[k]))      
    output.append(' '.join(counts_list))
  else:
    output.append(str(task))
  print('\t'.join(output))

if args.timings:
  for task_name in ordered_tasks:
    output = ['%s seconds' % (task_name)]
    timing = timings[task_name]
    if isinstance(timing, dict):
      for k in sorted(timing.keys()):
        output.append(timing[k])
    else:
      output.append(timing)
    print('\t'.join(str(v) for v in output))

l.debug('%s end' % (script_path))
