from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name='wolsey',
  version='0.0.1',
  description='wolsey - utilities for Cromwell',
  long_description=long_description,
  url='',
  author='',
  author_email='',
  license='MIT',
  packages=find_packages(),
  extras_require={
    'dev': ['pytest', 'tox']
  },
  scripts= ['bin/wol-lsf_copy_files.py',
    'bin/wol-summarize_log.py',
    'bin/wol-summary_executions.py']
)
