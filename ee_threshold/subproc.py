import logging
import os
import re
import sys
import shutil
import subprocess
import tempfile
import argparse

from utils import cd, mkdirs

logger = logging.getLogger(__name__)
jobs = int(os.getenv('WHIZARD_THREADS', 24))
batches = int(os.getenv('WHIZARD_BATCHES', 24))

parser = argparse.ArgumentParser(description='Parallel Whizard scanner')
parser.add_argument('folder', help='The name of the folder with the run.sin')
parser.add_argument('scan_object', help='The sindarin object that should be scanned')
parser.add_argument('start', help='The start of the scan range')
parser.add_argument('end', help='The end of the scan range')
parser.add_argument('--stepsize', type=float, help='The stepsize of the scan')
parser.add_argument("-d", '--dryrun', action='store_true',
    help='Only create sindarins, dont run the whizard')

def replace_file(filename, scan_object, iterator):
  tmp_fh, tmp_file = tempfile.mkstemp()
  regex = re.compile(r"(" + scan_object + " = )(.*)")
  replace = lambda x: x.group(1) + str(iterator)
  with open(tmp_file,'w') as new_file:
    with open(filename) as old_file:
      for line in old_file:
        new_line = regex.sub(replace, line)
        new_file.write(new_line)
  os.close(tmp_fh)
  os.remove(filename)
  shutil.move(tmp_file, filename)

def whizard_run(whizard, sindarin):
  cmd = whizard + ' ' + sindarin
  process = subprocess.call(cmd, shell=True)

def run(iterator, args=None):
  sindarin = args.folder + '/run.sin'
  runfolder = args.folder + '-' + str(iterator)
  print runfolder
  mkdirs(runfolder)
  shutil.copyfile(sindarin, os.path.join(runfolder, 'run.sin'))
  with cd(runfolder):
    replace_file('run.sin', args.scan_object, iterator)
    if (not args.dryrun):
      whizard_run('whizard -r', 'run.sin')
