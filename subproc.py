import logging
import os
import re
import sys
import shutil
import subprocess
import tempfile
from time import sleep
from functools import partial
from utils import cd, mkdirs, remove

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

def create_integration_sindarin(integration_sindarin, template_sindarin,
    adaption_iterations, integration_iterations):
  iterations = 'iterations = ' + adaption_iterations + ':"gw",' + integration_iterations
  replace_line = lambda line: line.replace('#ITERATIONS', iterations)
  sed(template_sindarin, replace_line, new_file=integration_sindarin)

def sed(original, replace_line, new_file=None, write_to_top=''):
  overwrite = new_file == None
  tmp_fh, tmp_file = tempfile.mkstemp()
  with open(tmp_file, 'w') as new_f:
    with open(original) as old_f:
      new_f.write(write_to_top)
      for line in old_f:
        new_f.write(replace_line(line))
  os.close(tmp_fh)
  if overwrite:
    target = original
  else:
    target = new_file
  remove(target)
  shutil.move(tmp_file, target)

def replace_file(filename, samplename, i, batches, events_per_batch):
  sample = '$sample = "' + samplename + '"\n'
  seed = 'seed = ' + str(abs(hash(samplename)) % (10 ** 8)) + '\n'
  if events_per_batch == None:
    replace_func = partial(divider, batches=batches)
  else:
    replace_func = lambda x : x.group(1) + str(events_per_batch)
  replace_line = lambda line : events_re.sub(replace_func,
      line).replace('include("', 'include("../')
  sed(write_to_top = sample + seed)

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
  remove(os.path.join(runfolder, fifo))
  if (purpose == 'histograms'):
    subprocess.call ("mkfifo " + os.path.join (runfolder, fifo), shell=True) 
  with cd(runfolder):
    replace_file(sindarin, runfolder, proc_id, batches, events_per_batch)
    whizard_run(purpose, whizard, sindarin, fifo, proc_id, options=options, analysis=analysis)
