#!/usr/bin/env python

import os
import sys
import re
import argparse
import logging
from datetime import datetime

SCRIPT_PATH = os.path.abspath(__file__)
FORMAT = '[%(asctime)s] %(levelname)s %(message)s'
l = logging.getLogger()
lh = logging.StreamHandler()
lh.setFormatter(logging.Formatter(FORMAT))
l.addHandler(lh)
l.setLevel(logging.INFO)
d = l.debug; i = l.info; w = l.warning; e = l.error

DESCRIPTION = '''
'''

EPILOG = '''
'''

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter):
  pass
parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG,
  formatter_class=CustomFormatter)

parser.add_argument('log_output')
parser.add_argument('-v', '--verbose', action='store_true',
    help='Set logging level to DEBUG')

args = parser.parse_args()

if args.verbose:
  l.setLevel(logging.DEBUG)

d('%s begin', SCRIPT_PATH)

start = None
end = None
success = False
with open(args.log_output, 'r') as f:
  for l in f:
    m = re.match('Started at (.+)', l)
    if m:
      i(m.group(1))
      # %c is the "Locale appropriate date and time representation"
      # see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
      start = datetime.strptime(m.group(1), '%c')
      continue
    m = re.match('Results reported on (.+)', l)
    if m:
      i(m.group(1))
      end = datetime.strptime(m.group(1), '%c')
      continue
    m = re.match('Successfully completed.', l)
    if m:
      i(m.group(0))
      success = True
      break

if not start or not end:
  e('Could not parse start or end')
  sys.exit(1)

if not success:
  w('Could not parse successful completion')

td = end - start
print('Total time: %s' % (td))
print('Total hours: %0.2f' % (td.total_seconds()/60/60))
print('Total minutes: %0.2f' % (td.total_seconds()/60))
print('Total seconds: %0.2f' % (td.total_seconds()))

d('%s end', (SCRIPT_PATH))



