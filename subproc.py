import logging
import os
import re
import sys
import shutil
import subprocess
from numpy import logspace, arange
from time import sleep
from functools import partial
from utils import *
from termcolor import colored
from nose.tools import eq_, assert_almost_equal, raises

logger = logging.getLogger(__name__)

def fill_runs(proc_name, proc_dict):
  if proc_dict['purpose'] == 'events' or proc_dict['purpose'] == 'histograms':
    runs = [(b, proc_name, proc_dict) for b in range(proc_dict['batches'])]
  elif proc_dict['purpose'] == 'scan':
    try:
      start = float(proc_dict['start'])
      stop = float(proc_dict['stop'])
      stepsize = proc_dict['stepsize']
    except KeyError:
      fatal('Aborting: You want a scan but have not set start, stop and stepsize')
    if stepsize == 'logarithmic':
      step_range = logspace(start, stop, num=proc_dict.get('steps', 10),
          endpoint=True, base=10.0)
    else:
      step_range = arange(start, stop, float(stepsize))
    runs = [(b, proc_name, proc_dict) for b in step_range]
  elif proc_dict['purpose'] == 'integrate':
    runs = [(-1, proc_name, proc_dict)]
  elif proc_dict['purpose'] == 'disabled':
    runs = []
  else:
    raise Exception("fill_runs: Unknown purpose")
  return runs

def test_fill_runs_basic():
  proc_dict = {'purpose': 'events', 'batches': 2}
  proc_name = 'test'
  runs = fill_runs(proc_name, proc_dict)
  eq_(runs, [(0, proc_name, proc_dict), (1, proc_name, proc_dict)])

  proc_dict = {'purpose': 'scan', 'start': 0.1, 'stop': 0.2, 'stepsize': 0.05}
  runs = fill_runs(proc_name, proc_dict)
  expectation = [(0.1, proc_name, proc_dict), (0.15, proc_name, proc_dict)]
  for r, e in zip(runs, expectation):
    assert_almost_equal (r[0], e[0], places=4)
    eq_ (r[1:2], e[1:2])

  proc_dict = {'purpose': 'integrate'}
  runs = fill_runs(proc_name, proc_dict)
  eq_(runs, [(-1, proc_name, proc_dict)])

  proc_dict = {'purpose': 'disabled'}
  runs = fill_runs(proc_name, proc_dict)
  eq_(runs, [])

  proc_dict = {'purpose': 'scan', 'start': 1, 'stop': 2, 'stepsize': 'logarithmic', 'steps': 1}
  runs = fill_runs(proc_name, proc_dict)
  expectation = [(10, proc_name, proc_dict)]
  for r, e in zip(runs, expectation):
    assert_almost_equal (r[0], e[0], places=4)
    eq_ (r[1:2], e[1:2])

@raises(SystemExit)
def test_fill_runs_exception():
  proc_name = 'test'
  proc_dict = {'purpose': 'scan'}
  runs = fill_runs(proc_name, proc_dict)

def get_component_suffixes (sindarin):
  suffixes = ['Born', 'Real', 'Virtual']
  if fks_method_is_resonance(sindarin):
    suffixes += ['Mismatch']
  return suffixes

def get_scale_suffixes ():
  return ['central', 'low', 'high']

def append_scale_suffixes (proc_name):
  return [proc_name + '_' + s for s in get_scale_suffixes()]

def create_component_sindarin_names (sindarin):
  return [sindarin + '_' + s for s in get_component_suffixes (sindarin)]

def get_mandatory(proc_dict, key):
  try:
    return p[key]
  except KeyError:
    logger.fatal('Aborting: ' + key + 'is mandatory')

def get_combined_integration(filename):
  return get_logical('\?combined_nlo_integration', filename)

def is_nlo_calculation(filename):
  return grep("nlo_calculation *=", filename)

def test_is_nlo_calculation():
  from nose.tools import eq_
  filename = 'test_is_nlo_calculation'
  test = open(filename, "w")
  test.write('foo bar')
  test.close()
  eq_(is_nlo_calculation(filename), False)
  test = open(filename, "w")
  test.write('nlo_calculation = "Full"')
  test.close()
  eq_(is_nlo_calculation(filename), True)
  os.remove(filename)

def fks_method_is_resonance(filename):
  return get_string('\$fks_mapping_type', filename) == '"resonances"'

def replace_scale (factor, filename):
  # Needs to be adapted for arbitrary number of spaces
  original_scale = get_value("(scale *= *)(.*$)", filename)
  #Add brackets because scale expression can be a sum of variables
  replace_func = lambda l: l.replace (original_scale, '(' + original_scale + ') * ' + str (factor))
  sed(filename, replace_line=replace_func)

def replace_nlo_calc(part, filename):
  # Expects part  = 'Real', 'Born', etc as strings
  replace_func = lambda l : l.replace('"Full"', '"' + part +'"')
  sed(filename, replace_line=replace_func)

def replace_proc_id(part, filename):
  # Expects part  = 'Real', 'Born', etc as strings
  proc_id = get_value("(process +)(\w+)", filename)
  replace_func = lambda l : l.replace(proc_id, proc_id + '_' + part)
  sed(filename, replace_line=replace_func)

def multiply_sindarins (base_sindarin, template_sindarin, scaled, nlo_type):
  scaled_sindarins = None
  if scaled:
    scaled_sindarins = create_scale_sindarins (base_sindarin)
  if nlo_type == 'nlo':
    if scaled_sindarins != None:
      for sindarin in scaled_sindarins:
        create_nlo_component_sindarins (template_sindarin, sindarin)
    else:
      create_nlo_component_sindarins (template_sindarin, base_sindarin)


def test_replace_nlo_calc():
  from nose.tools import eq_
  filename = 'test_replace_nlo_calc'
  test = open(filename, "w")
  test.write('include("process_settings.sin")\n')
  test.write("process proc_nlo = e1, E1 => e2, E2\n")
  test.write("integrate (proc_nlo)")
  test.close()
  replace_proc_id('Real', filename)
  eq_(get_value("(process +)(\w+)", filename), 'proc_nlo_Real')
  test = open(filename, "r")
  expectation = ['include("process_settings.sin")\n',
                 "process proc_nlo_Real = e1, E1 => e2, E2\n",
                 "integrate (proc_nlo_Real)"]
  for t, e in zip(test, expectation):
    eq_(t, e)
  test.close()
  os.remove(filename)

def replace_iterations (adaption_iterations, integration_iterations):
  iterations = 'iterations = ' + adaption_iterations + ':"gw"'
  if (integration_iterations != ' '):
    iterations += ',' + integration_iterations
  return lambda line: line.replace('#ITERATIONS', iterations)

def create_integration_sindarin(integration_sindarin, template_sindarin,
    adaption_iterations, integration_iterations):
  replace_line = replace_iterations (adaption_iterations, integration_iterations)
  sed(template_sindarin, replace_line, new_file=integration_sindarin)

def create_simulation_sindarin (simulation_sindarin, template_sindarin, process,
   adaption_iterations, integration_iterations, n_events):
  replace_line = replace_iterations (adaption_iterations, integration_iterations)
  sed(template_sindarin, replace_line, new_file=simulation_sindarin)
  command = 'n_events = ' + str (n_events) + '\n' \
          + 'checkpoint = n_events / 20' + '\n' \
          + 'simulate(' + process + ')'
  sed(simulation_sindarin, write_to_bottom=command)

def insert_suffix (sindarin, suffix):
  if 'integrate' in sindarin:
    return sindarin.replace('-integrate.sin', '_' + suffix + '-integrate.sin')
  else:
    return sindarin.replace('.sin', '_' + suffix + '.sin')


def create_scale_sindarins (base_sindarin):
  new_sindarins = []
  for suffix in get_scale_suffixes ():
    new_sindarin = insert_suffix (base_sindarin, suffix)
    new_sindarins.append(new_sindarin)
    shutil.copyfile (base_sindarin, new_sindarin)
    if suffix == 'low':
      replace_scale (0.5, new_sindarin)
    elif suffix == 'high':
      replace_scale (2.0, new_sindarin)
    replace_proc_id (suffix, new_sindarin)
  return new_sindarins
    

def create_nlo_component_sindarins (template_sindarin, base_sindarin):
  for suffix in get_component_suffixes (template_sindarin):
    new_sindarin = insert_suffix (base_sindarin, suffix)
    shutil.copyfile(base_sindarin, new_sindarin)
    replace_nlo_calc (suffix, new_sindarin)
    replace_proc_id (suffix, new_sindarin)

def get_grid_index (proc_name):
  words = proc_name.split ('_')
  grid_indices = {'Born': 1, 'Real': 2, 'Virtual': 3, 'Mismatch': 4}
  return grid_indices[words[len(words)-1]]

def divider(matchobj, batches):
  nevents = matchobj.group(2)
  divided = str(int(float(matchobj.group(2)) / batches))
  return matchobj.group(1) + divided + matchobj.group(3)

events_re = re.compile(r"(n_events = )([0-9]*)( \* K)")
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
    fatal('Exception occured: ' + str(e) + 'Whizard failed on executing ' + sindarin + num)
  else:
    if not grep('FATAL ERROR', 'whizard.log'):
      logger.info('Whizard finished' + num)
      with open('done', 'a'):
        os.utime('done', None)
    else:
      fatal('FATAL ERROR in whizard.log of ' + sindarin + num)

def generate(proc_name, proc_id, proc_dict, whizard, integration_grids, analysis=''):
  purpose = proc_dict['purpose']
  options = proc_dict.get('whizard_options', '--no-banner')
  sindarin = proc_name + '.sin'
  runfolder = proc_name + '-' + str(proc_id)
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
    integration_sindarin = proc_name + '-integrate.sin'
    sed(integration_sindarin, replace_line, new_file=os.path.join(runfolder, sindarin))
    with cd(runfolder):
      whizard_run(purpose, whizard, sindarin, proc_id=proc_id, options=options)
