import logging
import os
import re
import sys
import shutil
import subprocess
from time import sleep
from functools import partial
from utils import cd, mkdirs, remove, sed, grep, get_value

logger = logging.getLogger(__name__)
default_batches = int(os.getenv('WHIZARD_BATCHES', 64))
events_re = re.compile(r"(n_events = )([0-9]*)( \* K)")

def get_mandatory(proc_dict, key):
  try:
    return p[key]
  except KeyError:
    logger.fatal('Aborting: ' + key + 'is mandatory')

def get_combined_integration(filename):
  return get_logical('?combined_integration', filename)

def get_fks_method(filename):
  return get_string('$fks_method', filename)

def replace_nlo_calc(part, filename):
  # Expects part  = 'Real', 'Born', etc as strings
  replace_func = lambda l : l.replace('"Full"', '"' + part +'"')
  sed(filename, replace_line=replace_func)

def replace_proc_id(part, filename):
  # Expects part  = 'Real', 'Born', etc as strings
  proc_id = get_value("(process *)(\w*)", filename)
  replace_func = lambda l : l.replace(proc_id, proc_id + '_' + part)
  sed(filename, replace_line=replace_func)

def test_replace_nlo_calc():
  from nose.tools import eq_
  filename = 'test_replace_nlo_calc'
  test = open(filename, "w")
  test.write("process proc_nlo = e1, E1 => e2, E2\n")
  test.write("integrate (proc_nlo)")
  test.close()
  replace_proc_id('Real', filename)
  eq_(get_value("(process *)(\w*)", filename), 'proc_nlo_Real')
  test = open(filename, "r")
  expectation = ["process proc_nlo_Real = e1, E1 => e2, E2\n",
                 "integrate (proc_nlo_Real)"]
  for t, e in zip(test, expectation):
    eq_(t, e)
  test.close()
  os.remove(filename)

def divider(matchobj, batches):
  nevents = matchobj.group(2)
  divided = str(int(float(matchobj.group(2)) / batches))
  return matchobj.group(1) + divided + matchobj.group(3)

def replace_iterations (adaption_iterations, integration_iterations):
  iterations = 'iterations = ' + adaption_iterations + ':"gw",' + integration_iterations
  return lambda line: line.replace('#ITERATIONS', iterations)

def create_integration_sindarin(integration_sindarin, template_sindarin,
    adaption_iterations, integration_iterations):
  replace_line = replace_iterations (adaption_iterations, integration_iterations)
  sed(template_sindarin, replace_line, new_file=integration_sindarin)

def create_simulation_sindarin (simulation_sindarin, template_sindarin, process):
  command = 'simulate(' + process + ')'
  sed(template_sindarin, new_file=simulation_sindarin, 
     write_to_bottom=command)

def change_sindarin_for_event_gen(filename, samplename, i, proc_dict):
  sample = '$sample = "' + samplename + '"\n'
  seed = 'seed = ' + str(abs(hash(samplename)) % (10 ** 8)) + '\n'
  events_per_batch = proc_dict ['events_per_batch']
  if events_per_batch == None:
    replace_func = partial(divider, batches=proc_dict ['batches'])
  else:
    replace_func = lambda x : x.group(1) + str(events_per_batch)
  replace_line = lambda line : events_re.sub(replace_func,
      line).replace('include("', 'include("../')
  sed(filename, replace_line, write_to_top = sample + seed)

def whizard_run(purpose, whizard, sindarin, fifo=None, proc_id=None, options='', analysis=''):
  cmd = whizard + ' ' + sindarin + ' ' + options
  if (purpose == 'histograms'):
    yoda_file = '../../rivet/' + fifo.replace ('hepmc', 'yoda')
    cmd = cmd + ' & rivet --quiet --pwd -H ' + yoda_file + ' -a ' + analysis + ' ' + fifo
  num = ' in ' + str(proc_id) if proc_id != None else ''
  logger.info('Running ' + cmd + num)
  try:
    process = subprocess.call(cmd, shell=True)
  except Exception as e:
    logger.fatal('Exception occured: ' + str(e))
    logger.fatal('Whizard failed')
    sys.exit(1)
  else:
    if not grep('FATAL ERROR', 'whizard.log'):
      logger.info('Whizard finished' + num)
      with open('done', 'a'):
        os.utime('done', None)
    else:
      logger.fatal('FATAL ERROR in whizard.log')
      logger.fatal('Whizard failed')
      sys.exit(1)

def generate(proc_name, proc_id, proc_dict, whizard, integration_grids, analysis=''):
  purpose = proc_dict['purpose']
  options = proc_dict.get('whizard_options', '--no-banner')
  #process = proc_dict['process']
  #sindarin = proc_dict['process'] + '.sin'
  sindarin = proc_name + '.sin'
  #runfolder = process + '-' + str(proc_id)
  runfolder = proc_name + '-' + str(proc_id)
  #fifo = process + '-' + str(proc_id) + '.hepmc'
  fifo = proc_name + '-' + str(proc_id) + '.hepmc'
  event_generation = purpose == 'events' or purpose == 'histograms'
  mkdirs(runfolder)
  if event_generation:
    shutil.copyfile(sindarin, os.path.join(runfolder, sindarin))
    shutil.copyfile(integration_grids, os.path.join(runfolder, integration_grids))
    with cd(runfolder):
      if (purpose == 'histograms'):
        remove(fifo)
        subprocess.call ("mkfifo " + fifo, shell=True)
      change_sindarin_for_event_gen(sindarin, runfolder, proc_id, proc_dict)
      whizard_run(purpose, whizard, sindarin, fifo=fifo, proc_id=proc_id, options=options,
          analysis=analysis)
  else:
    scan_expression = proc_dict['scan_object'] + " = " + str(proc_id)
    replace_line = lambda line: line.replace('#SETSCAN',
      scan_expression).replace('include("', 'include("../')
    #integration_sindarin = process + '-integrate.sin'
    integration_sindarin = proc_name + '-integrate.sin'
    sed(integration_sindarin, replace_line, new_file=os.path.join(runfolder, sindarin))
    with cd(runfolder):
      whizard_run(purpose, whizard, sindarin, proc_id=proc_id, options=options)
