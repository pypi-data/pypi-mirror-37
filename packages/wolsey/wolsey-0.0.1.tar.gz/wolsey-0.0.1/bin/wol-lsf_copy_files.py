#!/usr/bin/env python

import sys
import os
import argparse
import pathlib
import shutil

def pmsg (*m):
  print(m, file=sys.stderr, flush=True)

description = """
Copy diagnostic files from LSF/Cromwell output 
"""

epilog = """

If output directory is specified, will be created or error if it 
already exists


"""

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter):
  pass
parser = argparse.ArgumentParser(description=description, epilog=epilog,
    formatter_class=CustomFormatter)

parser.add_argument('input_directory', help='Input directory. Last two components should be the workflow name and run id')
parser.add_argument('--output-directory', '-o', help='Output directory. Directory to copy diagnostic files to')
args = parser.parse_args()

__, run_id = os.path.split(args.input_directory)
__, workflow_name = os.path.split(__)

pmsg('workflow_name', workflow_name)
pmsg('run_id', run_id)

if run_id.translate(str.maketrans('','','-abcdef0123456789')):
  raise SystemExit('ERROR run_id %s contains non-hex or - characters' \
      % (run_id))

if args.output_directory:
  output_d = args.output_directory
else:
  output_d = '_'.join((workflow_name, run_id))

try:
  os.makedirs(output_d)
except FileExistsError:
  pmsg('ERROR: directory %s exists, delete and rerun' % (output_d))
  sys.exit(1)

file_list = [ 'rc', 'script', 'script.submit', 'stderr', 'stderr.submit', 
    'stdout', 'stdout.submit' ]

paths = []

for f in file_list:
  paths += list(pathlib.Path(args.input_directory).glob('**/%s' % (f)))

for path in paths:
  output_f = str(path).replace(args.input_directory, output_d)
  pmsg(path)
  pmsg(output_f)
  os.makedirs(os.path.dirname(output_f), exist_ok=True)
  shutil.copyfile(path, output_f)



