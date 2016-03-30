import logging
import os
import re
import sys
import shutil
import jsonschema
import textwrap
import subprocess
from distutils import spawn
from mpi4py import MPI
from numpy import logspace, arange
from functools import partial
from utils import *
from termcolor import colored
from nose.tools import *

def fill_all_runs(run_json):
  runs = []
  for proc_dict in run_json['processes']:
    template = proc_dict['process'] + '-template'
    if proc_dict.get ('scale_variation', False):
      processes = append_scale_suffixes (proc_dict['process'])
    else:
      processes = [proc_dict['process']]
    for proc_name in processes:
      if proc_dict['nlo_type'] == 'nlo':
        for nlo_proc_name in create_nlo_component_names (proc_name, proc_dict):
          runs += fill_runs(nlo_proc_name, proc_dict)
      else:
        runs += fill_runs(proc_name, proc_dict)
  return runs

def mpi_load_json():
  try:
    process_folder = sys.argv[1]
  except:
    fatal('You have to give me the process directory as argument')
  json_file = os.path.join(process_folder, 'run.json')
  schema_file = os.path.join(process_folder, '../run-schema.json')
  logger.info('Trying to read: ' + schema_file)
  schema = load_json(schema_file)
  logger.info('Trying to read: ' + json_file)
  run_json = load_json(json_file)
  try:
    logger.error(jsonschema.exceptions.best_match(jsonschema.
        Draft4Validator(schema).iter_errors(run_json)).message)
  except:
    pass
  try:
    jsonschema.validate(run_json, schema)
  except jsonschema.exceptions.SchemaError as e:
    fatal('Failed to validate schema:\n' + str(e))
  except jsonschema.exceptions.ValidationError as e:
    fatal('Failed to validate json:\n' + str(e))
  logger.info('Found the following processes:')
  for p in run_json['processes']:
    logger.info(p['process'] + '\t[' + p['purpose'] + ']')
  return run_json

def log(action, batch, proc_dict):
  logger.info(textwrap.fill(action + ' batch ' + str(batch) + ' of '+ \
      str(proc_dict) + ' on ' + MPI.Get_processor_name()))

# TODO: (bcn 2016-03-30) slim the Whizard. would be nice to only have
# information and data how to run Whizard here
class Whizard():
  def __init__(self, run_json):
    self.binary = run_json['whizard']
    if not spawn.find_executable(self.binary):
      fatal('No valid whizard found. You gave whizard = ' + self.binary)
    else:
      logger.info('Using ' + self.binary)

  def execute(self, purpose, sindarin, fifo=None, proc_id=None, options='', analysis=''):
    cmd = self.binary + ' ' + sindarin + ' ' + options
    if (purpose == 'histograms'):
      cmd = 'export RIVET_ANALYSIS_PATH=../../rivet; ' + cmd
      yoda_file = '../../rivet/' + fifo.replace ('hepmc', 'yoda')
      cmd = cmd + ' & rivet --quiet -H ' + yoda_file + ' -a ' + analysis + ' ' + fifo
    num = ' in ' + str(proc_id) if proc_id != None else ''
    logger.info('Calling subprocess ' + cmd + num)
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

  def generate(self, proc_name, proc_id, proc_dict, integration_grids, analysis=''):
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
        self.execute(purpose, sindarin, fifo=fifo, proc_id=proc_id, options=options,
            analysis=analysis)
    else:
      scan_expression = proc_dict['scan_object'] + " = " + str(proc_id)
      replace_line = lambda line: line.replace('#SETSCAN',
        scan_expression).replace('include("', 'include("../')
      integration_sindarin = proc_name + '-integrate.sin'
      sed(integration_sindarin, replace_line, new_file=os.path.join(runfolder, sindarin))
      with cd(runfolder):
        self.execute(purpose, sindarin, proc_id=proc_id, options=options)

  def run_process(self, (proc_id, proc_name, proc_dict)):
    log('Trying', proc_id, proc_dict)
    integration_sindarin = proc_name + '-integrate.sin'
    if proc_dict['nlo_type'] == 'nlo':
      integration_grids = proc_name + '_m' + str (get_grid_index(proc_name)) + '.vg'
    else:
      integration_grids = proc_name + '_m1.vg'
    purpose = proc_dict['purpose']
    event_generation = purpose == 'events' or purpose == 'histograms'
    whizard_options = proc_dict.get('whizard_options', '--no-banner')
    with cd('whizard/'):
      if not os.path.exists(integration_grids) and event_generation:
        logger.error('Didnt find integration grids with name ' + integration_grids + \
             ', but you wanted events! Aborting! Please use "integrate" first')
        return
      elif purpose == 'integrate':
        logger.info('Generating the following integration grids: ' + integration_grids)
        whizard.execute(purpose,
            sindarin=integration_sindarin,
            options=whizard_options)
      else:
        if event_generation:
          logger.info('Using the following integration grids: ' + integration_grids)
        runfolder = proc_name + '-' + str(proc_id)
        if (not os.path.isfile(os.path.join(runfolder, 'done'))):
          analysis = proc_dict.get('analysis', '')
          self.generate(proc_name,
              proc_id,
              proc_dict,
              integration_grids=integration_grids,
              analysis=analysis)
          if (os.path.isfile(os.path.join(runfolder, 'done')) and \
              purpose == 'events'):
            os.rename(os.path.join(runfolder, runfolder) + '.hepmc',
                os.path.join("../rivet", runfolder + '.hepmc'))
          return
        else:
          logger.info('Skipping ' + runfolder + ' because done is found')

def setup_sindarins(proc_dict, batch=None):
  if proc_dict['purpose'] != 'disabled':
    logger.info('Setting up sindarins of ' + str(proc_dict))
    with cd('whizard/'):
      base_sindarin = proc_dict['process'] + '.sin'
      template_sindarin = base_sindarin.replace('.sin', '-template.sin')
      integration_sindarin = base_sindarin.replace('.sin', '-integrate.sin')
      template_present = os.path.isfile(template_sindarin)
      scan = proc_dict['purpose'] == 'scan'
      if scan and not template_present:
        fatal('You have to supply ' + template_sindarin + ' for a scan')
      elif not scan and not template_present:
        fallback = integration_sindarin + ' and ' + base_sindarin
        if os.path.isfile(integration_sindarin) and os.path.isfile(base_sindarin):
          logger.info('Didnt find ' + template_sindarin + ', will use ' + fallback)
          return
        else:
          fatal('Didnt find ' + template_sindarin + ' nor ' + fallback)
      if template_present:
        if proc_dict['purpose'] == 'integrate' or scan:
          create_integration_sindarin(integration_sindarin, template_sindarin,
              proc_dict['adaption_iterations'], proc_dict.get('integration_iterations', ' '))
          multiply_sindarins (integration_sindarin, proc_dict,
             proc_dict.get('scale_variation', False), proc_dict['nlo_type'])
        elif proc_dict['purpose'] == 'histograms' or proc_dict['purpose'] == 'events':
          create_simulation_sindarin(base_sindarin, template_sindarin,
              proc_dict['process'], proc_dict['adaption_iterations'],
              proc_dict.get('integration_iterations', ' '),
              proc_dict['events_per_batch'])
          multiply_sindarins (base_sindarin, proc_dict,
             proc_dict.get('scale_variation', False), proc_dict['nlo_type'])
  else:
    logger.info('Skipping ' + proc_dict['process'] + ' because it is disabled')

def setup_func():
  with open('test_nlo_base-template.sin', "w") as test:
    test.write('include("process_settings.sin")\n')
    test.write('process test_nlo_base = e1, E1 => e2, E2 {nlo_calculation = "Full"}\n')
    test.write('integrate (test_nlo_base)')

def teardown_func():
  os.remove('test_nlo_base-template.sin')

def fill_runs(proc_name, proc_dict):
  if proc_dict['purpose'] == 'events' or proc_dict['purpose'] == 'histograms':
    runs = [(b, proc_name, proc_dict) for b in range(proc_dict['batches'])]
  # TODO: (bcn 2016-03-30) this should be made impossible in the scheme
  elif proc_dict['purpose'] == 'scan':
    try:
      start = float(proc_dict['start'])
      stop = float(proc_dict['stop'])
      stepsize = proc_dict['stepsize']
    except KeyError:
      fatal('Aborting: You want a scan but have not set start, stop and stepsize')
    else:
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
  try:
    return runs
  except UnboundLocalError:
    return []

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

@raises(Exception)
def test_fill_runs_exception():
  proc_name = 'test'
  proc_dict = {'purpose': 'scan'}
  runs = fill_runs(proc_name, proc_dict)
  eq_ (runs, [])
  proc_dict = {'purpose': 'foo'}
  runs = fill_runs(proc_name, proc_dict)

def get_component_suffixes (proc_dict):
  suffixes = ['Born', 'Real', 'Virtual']
  if proc_dict.get('fks_method', 'default') == 'resonances':
    suffixes += ['Mismatch']
  return suffixes

def get_scale_suffixes ():
  return ['central', 'low', 'high']

def append_scale_suffixes (proc_name):
  return [proc_name + '_' + s for s in get_scale_suffixes()]

def test_append_scale_suffixes():
  proc_name = 'test'
  eq_(append_scale_suffixes(proc_name), ['test_central','test_low','test_high'])

def create_nlo_component_names (sindarin, proc_dict):
  return [sindarin + '_' + s for s in get_component_suffixes (proc_dict)]

def test_create_component_sindarin_names ():
  test_dict = {'fks_method': 'foo'}
  test_sindarin = "proc_nlo"
  eq_(create_nlo_component_names(test_sindarin, test_dict),
      ['proc_nlo_Born', 'proc_nlo_Real', 'proc_nlo_Virtual'])
  test_dict = {'fks_method': 'resonances'}
  eq_(create_nlo_component_names(test_sindarin, test_dict),
      ['proc_nlo_Born', 'proc_nlo_Real', 'proc_nlo_Virtual', 'proc_nlo_Mismatch'])

# TODO: (bcn 2016-03-29) is this used anywhere??? whats the purpose?
def get_full_proc_names (base_name, proc_dict): # pragma: no cover
  scaled = proc_dict.get ('scale_variation', False)
  nlo = proc_dict['nlo_type'] == 'nlo'
  if not scaled and not nlo:
    full_names = [base_name]
  else:
    if scaled:
      scaled_names = []
      for suffix in get_scale_suffixes ():
        scaled_names += [base_name + '_' + suffix]
    else:
      scaled_names = [base_name]
    if nlo:
      full_names = []
      for scaled_name in scaled_names:
          full_names += create_nlo_component_names (scaled_name, proc_dict)
    else:
      full_names = scaled_names
  return full_names

def test_get_full_proc_names():
  pass

def is_nlo_calculation(filename):
  return grep("nlo_calculation *=", filename)

@with_setup(setup_func, teardown_func)
def test_is_nlo_calculation():
  filename = 'test_is_nlo_calculation'
  with open(filename, "w") as test:
    test.write('foo bar')
  eq_(is_nlo_calculation(filename), False)
  eq_(is_nlo_calculation('test_nlo_base-template.sin'), True)
  os.remove(filename)

def replace_scale (factor, filename):
  original_scale = get_scale(filename)
  # Add brackets because scale expression can be a sum of variables
  replace_func = lambda l: l.replace (original_scale, '(' + original_scale + ') * ' + str (factor))
  sed(filename, replace_line=replace_func)

def test_replace_scale():
  filename = 'test_replace_scale'
  with open(filename, "w") as test:
    test.write('scale = mtop')
  replace_scale (3, filename)
  with open(filename, "r") as test:
    eq_(test.read(), 'scale = (mtop) * 3')

  with open(filename, "w") as test:
    test.write('scale = 2 * mtop + 3 mH')
  replace_scale (1.0/2, filename)
  with open(filename, "r") as test:
    eq_(test.read(), 'scale = (2 * mtop + 3 mH) * 0.5')

def replace_nlo_calc(part, filename):
  # Expects part  = 'Real', 'Born', etc as strings
  replace_func = lambda l : l.replace('"Full"', '"' + part +'"')
  sed(filename, replace_line=replace_func)

def insert_suffix_in_sindarin (sindarin, suffix):
  if 'integrate' in sindarin:
    return sindarin.replace('-integrate.sin', '_' + suffix + '-integrate.sin')
  else:
    return sindarin.replace('.sin', '_' + suffix + '.sin')

def test_insert_suffix_in_sindarin ():
  test_sindarin = "proc_nlo-integrate.sin"
  eq_(insert_suffix_in_sindarin(test_sindarin, "suffix"), "proc_nlo_suffix-integrate.sin")
  test_sindarin2 = "proc_nlo.sin"
  eq_(insert_suffix_in_sindarin(test_sindarin2, "suffix"), "proc_nlo_suffix.sin")

def create_nlo_component_sindarins (proc_dict, integration_sindarin):
  for suffix in get_component_suffixes (proc_dict):
    new_sindarin = insert_suffix_in_sindarin (integration_sindarin, suffix)
    shutil.copyfile(integration_sindarin, new_sindarin)
    replace_nlo_calc (suffix, new_sindarin)
    replace_proc_id (suffix, new_sindarin)

@with_setup(setup_func, teardown_func)
def test_create_nlo_component_sindarins():
  base_sindarin = 'test_nlo_base-template.sin'
  integration_sindarin = base_sindarin.replace('-template', '')
  shutil.copyfile(base_sindarin, integration_sindarin)
  proc_dict = {}
  create_nlo_component_sindarins(proc_dict, integration_sindarin)
  base = 'test_nlo_base_'
  suffixes = ['Born', 'Real', 'Virtual']
  sindarins = [base + s + '.sin' for s in suffixes]
  for filename, suffix in zip(sindarins, suffixes):
    proc_id = get_process(filename)
    eq_ (proc_id, base + suffix)
    os.remove(filename)

def is_valid_wizard_sindarin (proc_dict, template_sindarin):
  proc_id = get_process(template_sindarin)
  valid = proc_id == template_sindarin.replace('-template.sin', '')
  purpose = proc_dict['purpose']
  if purpose == 'scan':
    valid = valid and grep('#SETSCAN', template_sindarin)
  elif purpose == 'nlo' or purpose == 'nlo_combined':
    valid = valid and is_nlo_calculation(template_sindarin)
  return valid

@with_setup(setup_func, teardown_func)
def test_is_valid_wizard_sindarin():
  proc_dict = {'purpose': 'foo'}
  with open('test_nlo_wrong.sin', "w") as test:
    test.write('process proc_nlo = e1, E1 => e2, E2 {nlo_calculation = "Full"}\n')
  eq_ (is_valid_wizard_sindarin(proc_dict, 'test_nlo_wrong.sin'), False)

  eq_ (is_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'), True)

  proc_dict = {'purpose': 'scan'}
  eq_ (is_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'), False)

  replace_func = lambda l : l.replace('test_nlo_base', 'test_nlo_scan')
  sed('test_nlo_base-template.sin', replace_line=replace_func,
      new_file='test_nlo_scan-template.sin', write_to_top='#SETSCAN')
  eq_ (is_valid_wizard_sindarin(proc_dict, 'test_nlo_scan-template.sin'), True)

  proc_dict = {'purpose': 'nlo'}
  eq_ (is_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'), True)

  os.remove('test_nlo_wrong.sin')
  os.remove('test_nlo_scan-template.sin')

def check_for_valid_wizard_sindarin (proc_dict, template_sindarin):
  if not is_valid_wizard_sindarin (proc_dict, template_sindarin):
    fatal ('Given sindarin is invalid for intended use')

# TODO: (bcn 2016-03-30) this only executes but doesnt check.. maybe we can use raise?
def test_check_for_valid_wizard_sindarin ():
  proc_dict = {'purpose': 'foo'}
  check_for_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin')

  proc_dict = {'purpose': 'scan'}
  check_for_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin')

def create_scale_sindarins (base_sindarin):
  new_sindarins = []
  for suffix in get_scale_suffixes ():
    new_sindarin = insert_suffix_in_sindarin (base_sindarin, suffix)
    new_sindarins.append(new_sindarin)
    shutil.copyfile (base_sindarin, new_sindarin)
    if suffix == 'low':
      replace_scale (0.5, new_sindarin)
    elif suffix == 'high':
      replace_scale (2.0, new_sindarin)
    replace_proc_id (suffix, new_sindarin)
  return new_sindarins

def multiply_sindarins (integration_sindarin, proc_dict, scaled, nlo_type):
  scaled_sindarins = None
  if scaled:
    scaled_sindarins = create_scale_sindarins (integration_sindarin)
  if nlo_type == 'nlo':
    if scaled_sindarins != None:
      for sindarin in scaled_sindarins:
        create_nlo_component_sindarins (proc_dict, sindarin)
    else:
      create_nlo_component_sindarins (proc_dict, integration_sindarin)

def replace_proc_id(part, filename):
  # Expects part  = 'Real', 'Born', etc as strings
  proc_id = get_process(filename)
  replace_func = lambda l : l.replace(proc_id, proc_id + '_' + part)
  sed(filename, replace_line=replace_func)

@with_setup(setup_func, teardown_func)
def test_replace_proc_id():
  filename = 'test_replace_proc_id'
  shutil.copyfile('test_nlo_base-template.sin', filename)
  replace_proc_id('Real', filename)
  eq_(get_process(filename), 'test_nlo_base_Real')
  with open(filename, "r") as test:
    expectation = ['include("process_settings.sin")\n',
                   'process test_nlo_base_Real = e1, E1 => e2, E2 {nlo_calculation = "Full"}\n',
                   'integrate (test_nlo_base_Real)']
    for t, e in zip(test, expectation):
      eq_(t, e)
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
