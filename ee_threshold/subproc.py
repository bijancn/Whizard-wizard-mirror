import logging
import os
import re
import sys
import shutil
import subprocess
import tempfile
from time import sleep

from utils import cd, mkdirs

logger = logging.getLogger(__name__)
jobs = int(os.getenv('WHIZARD_THREADS', 32))
batches = int(os.getenv('WHIZARD_BATCHES', 32))

def replace_file(filename, samplename, sqrts):
  tmp_fh, tmp_file = tempfile.mkstemp()
  with open(tmp_file,'w') as new_file:
    with open(filename) as old_file:
      for line in old_file:
        new_file.write(line.replace('sqrts = 340.', 'sqrts = ' + str(sqrts)))
  os.close(tmp_fh)
  os.remove(filename)
  shutil.move(tmp_file, filename)

def whizard_run(whizard, sindarin):
  cmd = whizard + ' ' + sindarin
  process = subprocess.call(cmd, shell=True)

def run(sqrts, folder=None):
  print sqrts
  sindarin = folder + '/SM_tt_threshold_test.sin'
  runfolder = folder + '-' + str(sqrts)
  mkdirs(runfolder)
  shutil.copyfile(sindarin, os.path.join(runfolder, 'SM_tt_threshold_test.sin'))
  with cd(runfolder):
    replace_file('SM_tt_threshold_test.sin', runfolder, sqrts)
    whizard_run('whizard', 'SM_tt_threshold_test.sin')
