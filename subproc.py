import logging
import os
import re
import sys
import shutil
import subprocess
import tempfile
from time import sleep
from functools import partial
from utils import cd, mkdirs

logger = logging.getLogger(__name__)
default_batches = int(os.getenv('WHIZARD_BATCHES', 64))
events_re = re.compile(r"(n_events = )([0-9]*)( \* K)")

def fatal(message):
  logger.fatal('>>> ' + message + ' <<<')
  sys.exit(1)

def divider(matchobj, batches):
  nevents = matchobj.group(2)
  divided = str(int(float(matchobj.group(2)) / batches))
  return matchobj.group(1) + divided + matchobj.group(3)

def replace_file(filename, samplename, i, batches, events_per_batch):
  tmp_fh, tmp_file = tempfile.mkstemp()
  sample = '$sample = "' + samplename + '"\n'
  seed = 'seed = ' + str(abs(hash(samplename)) % (10 ** 8)) + '\n'
  if events_per_batch == None:
    replace_func = partial(divider, batches=batches)
  else:
    replace_func = lambda x : x.group(1) + str(events_per_batch)
  with open(tmp_file,'w') as new_file:
    with open(filename) as old_file:
      new_file.write(sample + seed)
      for line in old_file:
        new_file.write(events_re.sub(replace_func, line).replace('include("', 'include("../'))
  os.close(tmp_fh)
  os.remove(filename)
  shutil.move(tmp_file, filename)

def whizard_run(purpose, whizard, sindarin, fifo, proc_id=None, options='', analysis=''):
  print ('in whizard_run') ### Debugging
  ### Old command without Fifo
  cmd = whizard + ' ' + sindarin + ' ' + options
  if (purpose == 'histograms'):
 	 ### New command using Fifo
  	yoda_file = '../../rivet/' + fifo.replace ('hepmc', 'yoda')
  	cmd = cmd + ' & rivet --quiet --pwd -H ' + yoda_file + ' -a ' + analysis + ' ' + fifo
  num = ' on thread ' + str(proc_id) if proc_id != None else ''
  logger.info('Running ' + cmd + num)
  try:
    process = subprocess.call(cmd, shell=True)
  except Exception as e:
    logger.error('Exception occured: ' + str(e))
    logger.error('Whizard failed')
  else:
    logger.info('Whizard finished' + num)
    with open('done', 'a'):
      os.utime('done', None)

def run(proc_id, purpose, whizard, sindarin, integration_grids, batches=default_batches,
    options='', events_per_batch=None, analysis=''):
  process = sindarin.replace('.sin', '')
  runfolder = process + '-' + str(proc_id)
  fifo = process + '-' + str(proc_id) + '.hepmc'
  mkdirs(runfolder)
  ###fifo = os.path.join (runfolder, fifo)
  shutil.copyfile(sindarin, os.path.join(runfolder, sindarin))
  shutil.copyfile(integration_grids, os.path.join(runfolder, integration_grids))
  if (os.path.isfile (os.path.join (runfolder, fifo))):
	 os.remove (os.path.join (runfolder, fifo))
  if (purpose == 'histograms'):
	  subprocess.call ("mkfifo " + os.path.join (runfolder, fifo), shell=True) 
  with cd(runfolder):
    replace_file(sindarin, runfolder, proc_id, batches, events_per_batch)
    whizard_run(purpose, whizard, sindarin, fifo, proc_id, options=options, analysis=analysis)
