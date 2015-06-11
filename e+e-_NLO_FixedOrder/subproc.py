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
batches = 10
events_re = re.compile(r"(n_events = )([0-9]*)")

def divider(matchobj):
  nevents = matchobj.group(2)
  divided = str(int(float(matchobj.group(2)) / batches))
  return matchobj.group(1) + divided

def replace_file(filename, samplename, i):
  tmp_fh, tmp_file = tempfile.mkstemp()
  sample = '$sample = "' + samplename + '"\n'
  seed = 'seed = ' + str(abs(hash(samplename)) % (10 ** 8)) + '\n'
  with open(tmp_file,'w') as new_file:
    with open(filename) as old_file:
      new_file.write(sample + seed)
      for line in old_file:
        new_file.write(events_re.sub(divider, line).replace('include("', 'include("../'))
  os.close(tmp_fh)
  os.remove(filename)
  shutil.move(tmp_file, filename)

def whizard_run(whizard, sindarin, core=None):
  cmd = whizard + ' ' + sindarin + ' --rebuild-events'
  num = ' on thread ' + str(core) if core != None else ''
  logger.info('Running ' + cmd + num)
  try:
    process = subprocess.call(cmd, shell=True)
  except:
    logger.error('Exception occured: ' + str(exception))
    logger.error('Whizard failed')
  else:
    logger.info('Whizard finished')

def run(i, whizard, sindarin, integration_grids):
  process = sindarin.replace('.sin', '')
  runfolder = process + '-' + str(i)
  mkdirs(runfolder)
  shutil.copyfile(sindarin, os.path.join(runfolder, sindarin))
  shutil.copyfile(integration_grids, os.path.join(runfolder, integration_grids))
  with cd(runfolder):
    replace_file(sindarin, runfolder, i)
    whizard_run(whizard, sindarin, i)
