import os
import re
import shutil
import subprocess
import textwrap
import logging
# import unittest   # has decorator for skipping tests: @unittest.skip("reason")
from distutils import spawn
from functools import partial
from math import log10
import jsonschema
from mpi4py import MPI
from numpy import logspace, arange, log2
import nose.tools as nt
import utils as ut
# from termcolor import colored


def no_critical_log():
  logging.disable(logging.CRITICAL)


def fill_all_runs(_run_json):
  runs = []
  for proc_dict in _run_json['processes']:
    if proc_dict.get('scale_variation', False):
      processes = append_scale_suffixes(proc_dict['process'])
    else:
      processes = [proc_dict['process']]
    for proc_name in processes:
      if proc_dict['nlo_type'] == 'nlo':
        for nlo_proc_name in create_nlo_component_names(proc_name, proc_dict):
          runs += fill_runs(nlo_proc_name, proc_dict)
      else:
        runs += fill_runs(proc_name, proc_dict)
  return runs


def retrieve_and_validate_run_json(process_folder, json_name='run.json'):
  json_file = os.path.join(process_folder, json_name)
  schema_file = os.path.join(process_folder, '../run-schema.json')
  ut.logger.info('Trying to read: ' + schema_file)
  schema = ut.load_json(schema_file)
  ut.logger.info('Trying to read: ' + json_file)
  json = ut.load_json(json_file)
  try:
    ut.logger.error(jsonschema.exceptions.best_match
        (jsonschema.Draft4Validator(schema).iter_errors(json)).message)
  except:
    pass
  try:
    jsonschema.validate(json, schema)
  except jsonschema.exceptions.SchemaError as e:
    ut.fatal('Failed to validate schema:\n' + str(e))
  except jsonschema.exceptions.ValidationError as e:
    ut.fatal('Failed to validate json:\n' + str(e))
  json = expand_process(json)
  ut.logger.info('Found the following processes:')
  for p in json['processes']:
    ut.logger.info(p['process'] + '\t[' + p['purpose'] + ']')
  return json


def expand_process(run_json):
  for proc_dict in list(run_json['processes']):
    if type(proc_dict['process']) is list:
      for proc in proc_dict['process']:
        new_proc_dict = proc_dict.copy()
        new_proc_dict['process'] = proc
        run_json['processes'].append(new_proc_dict)
      run_json['processes'].remove(proc_dict)
    else:
      ut.logger.warning('Deprecated: Please use a list for process in the future')
  return run_json


def test_expand_process():
  test_proc_dict = {'processes': [{'process': 'test_A'}, {'process': 'test_B'}]}
  result = expand_process(test_proc_dict)
  nt.eq_(result, test_proc_dict)

  test_proc_dict = {'processes': [{'process': ['test_A', 'test_B'],
      'purpose': 'scan'}, {'process': 'test_B'}]}
  result = expand_process(test_proc_dict)
  expected = {'processes': [
      {'process': 'test_B'},
      {'process': 'test_A', 'purpose': 'scan'},
      {'process': 'test_B', 'purpose': 'scan'}]}
  nt.eq_(result, expected)


def log(action, batch, proc_dict):
  ut.logger.info(textwrap.fill(action + ' batch ' + str(batch) + ' of ' +
      str(proc_dict) + ' on ' + MPI.Get_processor_name()))


# TODO: (bcn 2016-03-30) slim the Whizard. would be nice to only have
# information and data how to run Whizard here
SUCCESS, FAIL = range(2)


class Whizard():
  def __init__(self, run_json, verbose):
    if not verbose:
      devnull = open(os.devnull, 'w')
      self.out = devnull
      self.err = devnull
      self.call = lambda cmd: subprocess.call(cmd, shell=True, stderr=self.err,
          stdout=self.out)
    else:
      self.call = lambda cmd: subprocess.call(cmd, shell=True)
    self.binary = run_json.get('whizard', 'whizard')
    if not spawn.find_executable(self.binary):
      ut.fatal('No valid whizard found. You gave whizard = ' + self.binary)
      self.call = lambda cmd : FAIL
    else:
      ut.logger.info('Using ' + self.binary)

  def execute(self, purpose, sindarin, fifo=None, proc_id=None, options='',
      analysis=''):
    cmd = 'nice -n 9 ' + self.binary + ' ' + sindarin + ' ' + options
    if (purpose == 'histograms'):
      cmd = 'export RIVET_ANALYSIS_PATH=../../rivet; ' + cmd
      yoda_file = '../../rivet/' + fifo.replace('hepmc', 'yoda')
      cmd = cmd + ' & rivet --quiet -H ' + yoda_file + ' -a ' + analysis + ' ' + fifo
    num = ' in ' + str(proc_id) if proc_id is not None else ''
    ut.logger.info('Calling subprocess ' + cmd + num)
    try:
      return_code = self.call(cmd)
    except Exception as e:
      ut.fatal('Exception occured: ' + str(e) + 'Whizard failed on executing ' +
          sindarin + num)
      return FAIL
    else:
      if not ut.grep('ERROR', 'whizard.log'):
        ut.logger.info('Whizard finished' + num)
        ut.touch('done')
        return return_code
      else:
        ut.fatal('ERROR in whizard.log of ' + sindarin + num)
        return FAIL

  def generate(self, proc_name, proc_id, proc_dict, integration_grids, analysis=''):
    purpose = proc_dict['purpose']
    options = proc_dict.get('whizard_options', '--no-banner')
    sindarin = proc_name + '.sin'
    runfolder = proc_name + '-' + str(proc_id)
    fifo = proc_name + '-' + str(proc_id) + '.hepmc'
    event_generation = purpose == 'events' or purpose == 'histograms'
    only_sindarins = proc_dict.get('only_sindarins', False)
    ut.mkdirs(runfolder)
    if not only_sindarins:
      _exe = lambda p: self.execute(p, sindarin, fifo=fifo, proc_id=proc_id,
            options=options, analysis=analysis)
    else:
      _exe = lambda p: SUCCESS
    if event_generation:
      shutil.copyfile(sindarin, os.path.join(runfolder, sindarin))
      shutil.copyfile(integration_grids, os.path.join(runfolder, integration_grids))
      with ut.cd(runfolder):
        if (purpose == 'histograms'):
          ut.remove(fifo)
          # Suppress annoying display output if Fifo is already present
          if not os.path.isfile(fifo):
            subprocess.call("mkfifo " + fifo, shell=True)
        change_sindarin_for_event_gen(sindarin, runfolder, proc_id, proc_dict)
        return _exe(purpose)
    elif purpose == 'scan':
      if '-' in str(proc_id):
        scan_value = str(proc_id).split('-')[0]
      else:
        scan_value = str(proc_id)
      scan_expression = proc_dict['scan_object'] + " = " + scan_value
      replace_line = lambda line: line.replace('#SETSCAN',
        scan_expression).replace('include("', 'include("../')
      integration_sindarin = proc_name + '-integrate.sin'
      ut.sed(integration_sindarin, replace_line,
          new_file=os.path.join(runfolder, sindarin))
      with ut.cd(runfolder):
        set_seed(sindarin, runfolder)
        return _exe(purpose)
    elif purpose == 'test_soft':
      options = options + ' --debug subtraction '
      replace_line = lambda line: line.replace('include("', 'include("../')
      integration_sindarin = proc_name + '-integrate.sin'
      target_sindarin = os.path.join(runfolder, sindarin)
      ut.sed(integration_sindarin, replace_line=replace_line,
          write_to_top='?test_soft_limit = true\n',
          new_file=target_sindarin)
      replace_nlo_calc('Real', target_sindarin)
      with ut.cd(runfolder):
        return _exe(purpose)
    else:
      raise NotImplementedError

  def run_process(self, (proc_id, proc_name, proc_dict)):
    log('Trying', proc_id, proc_dict)
    if proc_dict['nlo_type'] == 'nlo':
      beam_type = proc_dict.get('beam_type', 'leptons')
      index = get_grid_index(proc_name, beam_type)
      integration_grids = proc_name + '_m' + str(index) + '.vg'
    else:
      integration_grids = proc_name + '_m1.vg'
    purpose = proc_dict['purpose']
    event_generation = purpose == 'events' or purpose == 'histograms'
    with ut.cd('whizard/'):
      if not os.path.exists(integration_grids) and event_generation:
        ut.logger.error('Didnt find integration grids with name ' + integration_grids +
             ', but you wanted events! Aborting! Please use "integration" first')
        return FAIL
      elif purpose == 'integration':
        ut.logger.info('Generating the following integration grids: ' +
            integration_grids)
        integration_sindarin = proc_name + '-integrate.sin'
        whizard_options = proc_dict.get('whizard_options', '--no-banner')
        return self.execute(purpose,
            sindarin=integration_sindarin,
            options=whizard_options)
      else:
        if event_generation:
          ut.logger.info('Using the following integration grids: ' + integration_grids)
        runfolder = proc_name + '-' + str(proc_id)
        if (not os.path.isfile(os.path.join(runfolder, 'done'))):
          analysis = proc_dict.get('analysis', '')
          return_code = self.generate(proc_name,
              proc_id,
              proc_dict,
              integration_grids=integration_grids,
              analysis=analysis)
          if return_code == SUCCESS:
            return_code = self.handle_results(runfolder, purpose)
          return return_code
        else:
          ut.logger.info('Skipping ' + runfolder + ' because done is found')
          return SUCCESS

  def handle_results(self, runfolder, purpose):
    done = os.path.isfile(os.path.join(runfolder, 'done'))
    if (done and purpose == 'events'):
      os.rename(os.path.join(runfolder, runfolder) + '.hepmc',
          os.path.join("../rivet", runfolder + '.hepmc'))
    if (done and purpose == 'test_soft'):
      ut.mkdirs("../scan-results")
      soft_log = os.path.join(runfolder, 'soft.log')
      if os.path.isfile(soft_log):
        os.rename(soft_log, os.path.join("../scan-results",
          runfolder.strip('--1') + '.soft.dat'))
      else:
        return FAIL
    return SUCCESS


def setup_sindarins(run_json):
  for p in run_json['processes']:
    setup_sindarin(p)


def setup_sindarin(proc_dict):
  if not proc_dict.get('disabled', False):
    ut.logger.info('Setting up sindarins of ' + str(proc_dict))
    whizard_folder = 'whizard'
    with ut.cd(whizard_folder):
      base_sindarin = proc_dict['process'] + '.sin'
      template_sindarin = base_sindarin.replace('.sin', '-template.sin')
      check_for_valid_wizard_sindarin(proc_dict, template_sindarin)
      integration_sindarin = base_sindarin.replace('.sin', '-integrate.sin')
      template_present = os.path.isfile(template_sindarin)
      scan = proc_dict['purpose'] == 'scan'
      test_soft = proc_dict['purpose'] == 'test_soft'
      if scan and not template_present:
        ut.fatal('You have to supply ' + template_sindarin + ' for a scan')
      elif not scan and not template_present:
        fallback = integration_sindarin + ' and ' + base_sindarin
        if os.path.isfile(integration_sindarin) and os.path.isfile(base_sindarin):
          ut.logger.info('Didnt find ' + template_sindarin + ', will use ' + fallback)
          return
        else:
          ut.fatal('Didnt find ' + template_sindarin + ' nor ' + fallback)
      if template_present:
        if proc_dict['purpose'] == 'integration' or scan or test_soft:
          create_integration_sindarin(integration_sindarin, template_sindarin,
              proc_dict['process'], proc_dict['adaption_iterations'],
              proc_dict.get('integration_iterations', ' '))
          multiply_sindarins(integration_sindarin, proc_dict,
             proc_dict.get('scale_variation', False), proc_dict['nlo_type'])
        elif proc_dict['purpose'] == 'histograms' or proc_dict['purpose'] == 'events':
          create_simulation_sindarin(base_sindarin, template_sindarin,
              proc_dict['process'], proc_dict['adaption_iterations'],
              proc_dict.get('integration_iterations', ' '),
              proc_dict['events_per_batch'])
          multiply_sindarins(base_sindarin, proc_dict,
             proc_dict.get('scale_variation', False), proc_dict['nlo_type'])
  else:
    ut.logger.info('Skipping ' + proc_dict['process'] + ' because it is disabled')


def create_test_nlo_base():
  with open('test_nlo_base-template.sin', "w") as test:
    test.write('include("process_settings.sin")\n')
    test.write('process test_nlo_base = e1, E1 => e2, E2 {nlo_calculation = "Full"}\n')
    test.write('integrate (test_nlo_base)')


def remove_test_nlo_base():
  os.remove('test_nlo_base-template.sin')


def get_steps(scan, start, stop):
  try:
    steps = scan['steps']
    stepsize = (stop - start) / steps
  except KeyError:
    stepsize = scan['stepsize']
    steps = (stop - start) / stepsize
  except KeyError:
    ut.fatal('Aborting: You have to give either steps or stepsize')
  return steps, stepsize


def get_step_range(scan_type, start, stop, steps, stepsize):
  if scan_type == 'logarithmic':
    step_range = logspace(log10(start), log10(stop), num=steps,
        endpoint=True, base=10.0)
  elif scan_type == 'logarithmic2':
    step_range = logspace(log2(start), log2(stop), num=steps,
        endpoint=True, base=2.0)
  elif scan_type == 'linear':
    step_range = arange(start, stop, float(stepsize))
  else:
    ut.fatal('Aborting: Unknown scan type')
  return step_range


def fill_scan_runs(proc_name, proc_dict, scans):
  runs = []
  try:
    scan_object = proc_dict['scan_object']
  except KeyError:
    ut.fatal('Aborting: You want a scan but have not set a scan_object')
    raise
  for scan in scans:
    start = float(scan['start'])
    stop = float(scan['stop'])
    scan_type = scan['type']
    steps, stepsize = get_steps(scan, start, stop)
    step_range = get_step_range(scan_type, start, stop, steps, stepsize)
    if proc_dict.get('integration_copies', 1) > 1:
      runs += get_process_copies(proc_name, proc_dict, step_range)
    else:
      runs += [(str(sr) + '-' + scan_object, proc_name, proc_dict) for sr in step_range]
  return runs


def try_fill_scan_runs(proc_name, proc_dict):
  try:
    scans = proc_dict['ranges']
  # TODO: (bcn 2016-03-30) this should be made impossible in the scheme
  except KeyError:
    ut.fatal('Aborting: You want a scan but have not set a ranges array')
    return []
  else:
    return fill_scan_runs(proc_name, proc_dict, scans)


def fill_runs(proc_name, proc_dict):
  purpose = proc_dict['purpose']
  if proc_dict.get('disabled', False):
    runs = []
  elif purpose == 'events' or purpose == 'histograms':
    runs = [(b, proc_name, proc_dict) for b in range(proc_dict['batches'])]
  elif purpose == 'scan':
    runs = try_fill_scan_runs(proc_name, proc_dict)
  elif purpose == 'integration' or purpose == 'test_soft':
    runs = [(-1, proc_name, proc_dict)]
  else:
    raise Exception("fill_runs: Unknown purpose: " + purpose)
  try:
    return runs
  except UnboundLocalError:
    return []


def test_fill_runs_basic():
  proc_dict = {'purpose': 'events', 'batches': 2}
  proc_name = 'test'
  runs = fill_runs(proc_name, proc_dict)
  nt.eq_(runs, [(0, proc_name, proc_dict), (1, proc_name, proc_dict)])

  proc_dict = {'purpose': 'scan', 'scan_object': 'sqrts', 'ranges':
      [{'start': 0.1, 'stop': 0.2, 'stepsize': 0.05, 'type': 'linear'}]}
  runs = fill_runs(proc_name, proc_dict)
  expectation = [('0.1-sqrts', 'test', proc_dict), ('0.15-sqrts', 'test', proc_dict)]
  for r, e in zip(runs, expectation):
    nt.eq_(r[0:2], e[0:2])

  proc_dict = {'purpose': 'integration'}
  runs = fill_runs(proc_name, proc_dict)
  nt.eq_(runs, [(-1, proc_name, proc_dict)])

  proc_dict = {'purpose': 'histograms', 'disabled': True}
  runs = fill_runs(proc_name, proc_dict)
  nt.eq_(runs, [])

  proc_dict = {'purpose': 'scan', 'scan_object': 'sqrts',
      'ranges': [{'start': 1, 'stop': 10, 'type': 'logarithmic', 'steps': 2}]}
  runs = fill_runs(proc_name, proc_dict)
  expectation = [('1.0-sqrts', 'test', proc_dict), ('10.0-sqrts', 'test', proc_dict)]
  nt.eq_(len(runs), len(expectation))
  for r, e in zip(runs, expectation):
    nt.eq_(r[0:2], e[0:2])


@nt.raises(Exception)
@nt.with_setup(no_critical_log)
def test_fill_runs_exception():
  proc_name = 'test'
  proc_dict = {'purpose': 'scan'}
  runs = fill_runs(proc_name, proc_dict)
  nt.eq_(runs, [])
  proc_dict = {'purpose': 'foo'}
  runs = fill_runs(proc_name, proc_dict)


def get_component_suffixes(proc_dict):
  suffixes = ['Born', 'Real', 'Virtual']
  if proc_dict.get('fks_method', 'default') == 'resonances':
    suffixes += ['Mismatch']
  if proc_dict.get('beam_type', 'leptons') == 'hadrons':
    suffixes += ['Dglap']
  return suffixes


def get_scale_suffixes():
  return ['central', 'low', 'high']


def append_scale_suffixes(proc_name):
  return [proc_name + '_' + s for s in get_scale_suffixes()]


def get_process_copies(proc_name, proc_dict, step_range):
  runs = []
  for i_copy in range(proc_dict.get('integration_copies', 1)):
    runs += [(str(b) + '-' + str(i_copy), proc_name, proc_dict) for b in step_range]
  return runs


def test_append_scale_suffixes():
  proc_name = 'test'
  nt.eq_(append_scale_suffixes(proc_name),
      ['test_central', 'test_low', 'test_high'])


def create_nlo_component_names(sindarin, proc_dict):
  return [sindarin + '_' + s for s in get_component_suffixes(proc_dict)]


def test_create_component_sindarin_names():
  test_dict = {'fks_method': 'foo'}
  test_sindarin = "proc_nlo"
  nt.eq_(create_nlo_component_names(test_sindarin, test_dict),
      ['proc_nlo_Born', 'proc_nlo_Real', 'proc_nlo_Virtual'])
  test_dict = {'fks_method': 'resonances'}
  nt.eq_(create_nlo_component_names(test_sindarin, test_dict),
      ['proc_nlo_Born', 'proc_nlo_Real', 'proc_nlo_Virtual', 'proc_nlo_Mismatch'])


def is_nlo_calculation(filename):
  return ut.grep("nlo_calculation *=", filename)


@nt.with_setup(create_test_nlo_base, remove_test_nlo_base)
def test_is_nlo_calculation():
  filename = 'test_is_nlo_calculation'
  with open(filename, "w") as test:
    test.write('foo bar')
  nt.eq_(is_nlo_calculation(filename), False)
  nt.eq_(is_nlo_calculation('test_nlo_base-template.sin'), True)
  os.remove(filename)


def replace_scale(factor, filename):
  original_scale = ut.get_scale(filename)
  # Add brackets because scale expression can be a sum of variables
  replace_func = lambda l: l.replace(original_scale,
      '(' + original_scale + ') * ' + str(factor))
  ut.sed(filename, replace_line=replace_func)


def check_for_n_events(line, new_n_events):
  if 'n_events = ' in line:
     line_split = line.split()
     return line_split[0] + ' = ' + str(new_n_events) + '\n'
  else:
     return line


def replace_n_events(factor, filename):
  original_n_events = ut.get_n_events(filename)
  if original_n_events is not None:
    new_n_events = factor * int(original_n_events)
    replace_func = lambda l: check_for_n_events(l, new_n_events)
    ut.sed(filename, replace_line=replace_func)


def test_replace_scale():
  filename = 'test_replace_scale'
  with open(filename, "w") as test:
    test.write('scale = mtop')
  replace_scale(3, filename)
  with open(filename, "r") as test:
    nt.eq_(test.read(), 'scale = (mtop) * 3')

  with open(filename, "w") as test:
    test.write('scale = 2 * mtop + 3 mH')
  replace_scale(1.0 / 2, filename)
  with open(filename, "r") as test:
    nt.eq_(test.read(), 'scale = (2 * mtop + 3 mH) * 0.5')
  os.remove('test_replace_scale')


def replace_nlo_calc(part, filename):
  # Expects part  = 'Real', 'Born', etc as strings
  replace_func = lambda l : l.replace('"Full"', '"' + part + '"')
  ut.sed(filename, replace_line=replace_func)


def insert_suffix_in_sindarin(sindarin, suffix):
  if 'integrate' in sindarin:
    return sindarin.replace('-integrate.sin', '_' + suffix + '-integrate.sin')
  else:
    return sindarin.replace('.sin', '_' + suffix + '.sin')


def test_insert_suffix_in_sindarin():
  test_sindarin = "proc_nlo-integrate.sin"
  nt.eq_(insert_suffix_in_sindarin(test_sindarin, "suffix"),
      "proc_nlo_suffix-integrate.sin")
  test_sindarin2 = "proc_nlo.sin"
  nt.eq_(insert_suffix_in_sindarin(test_sindarin2, "suffix"), "proc_nlo_suffix.sin")


def create_nlo_component_sindarins(proc_dict, integration_sindarin, all_sindarins=''):
  for suffix in get_component_suffixes(proc_dict):
    new_sindarin = insert_suffix_in_sindarin(integration_sindarin, suffix)
    shutil.copyfile(integration_sindarin, new_sindarin)
    replace_nlo_calc(suffix, new_sindarin)
    replace_proc_id(suffix, new_sindarin)
    event_mult = proc_dict.get('event_mult_real', 1)
    if event_mult != 1 and "Real" in new_sindarin:
      replace_n_events(event_mult, new_sindarin)


def get_all_sindarin_names(integration_sindarin, proc_dict):
  all_sindarins = []
  if proc_dict.get('scale_variation', False):
     scaled_sindarins = create_scale_sindarins(integration_sindarin, proc_dict)
  else:
     scaled_sindarins = [integration_sindarin]
  for ssindarin in scaled_sindarins:
    for suffix in get_component_suffixes(proc_dict):
      new_sindarin = insert_suffix_in_sindarin(ssindarin, suffix)
      all_sindarins.append(new_sindarin)
  return all_sindarins


@nt.with_setup(create_test_nlo_base, remove_test_nlo_base)
def test_create_nlo_component_sindarins():
  template_sindarin = 'test_nlo_base-template.sin'
  base_sindarin = template_sindarin.replace('-template', '')
  shutil.copyfile(template_sindarin, base_sindarin)
  proc_dict = {}
  create_nlo_component_sindarins(proc_dict, base_sindarin)
  base = 'test_nlo_base_'
  suffixes = ['Born', 'Real', 'Virtual']
  sindarins = [base + s + '.sin' for s in suffixes]
  for filename, suffix in zip(sindarins, suffixes):
    proc_id = ut.get_process(filename)
    nt.eq_(proc_id, base + suffix)
    os.remove(filename)
  os.remove('test_nlo_base.sin')


def is_valid_wizard_sindarin(proc_dict, template_sindarin):
  purpose = proc_dict['purpose']
  proc_id = ut.get_process(template_sindarin)
  valid = True
  if proc_id != 'PROCESS' and \
      proc_id != template_sindarin.replace('-template.sin', ''):
    ut.fatal('The process doesnt have the same name as the file')
    valid = False
  if purpose == 'scan' and not ut.grep('#SETSCAN', template_sindarin):
    ut.fatal('Your purpose is scan but the sindarin has no #SETSCAN')
    valid = False
  elif (purpose == 'nlo' or purpose == 'nlo_combined') and \
      not is_nlo_calculation(template_sindarin):
    ut.fatal('Your purpose is nlo* but the sindarin has no nlo command')
    valid = False
  fks_mapping = ut.get_string("fks_mapping_type", template_sindarin)
  resonance_set_in_sindarin = fks_mapping == '"resonances"'
  fks_method = proc_dict.get('fks_method', 'default')
  resonance_not_set_in_json = fks_method != 'resonances'
  if resonance_set_in_sindarin and resonance_not_set_in_json:
    ut.fatal('You set fks_mapping_type to resonances but havent set it in the run.json')
    valid = False
  return valid


@nt.with_setup(create_test_nlo_base, remove_test_nlo_base)
def test_is_valid_wizard_sindarin():
  proc_dict = {'purpose': 'foo'}
  with open('test_nlo_wrong.sin', "w") as test:
    test.write('process proc_nlo = e1, E1 => e2, E2 {nlo_calculation = "Full"}\n')
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_wrong.sin'), False)

  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'),
      True, "test_nlo_base should work with purpose foo")

  proc_dict = {'purpose': 'scan'}
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'),
      False, "test_nlo_base should not work with purpose scan")

  replace_func = lambda l : l.replace('test_nlo_base', 'test_nlo_scan')
  ut.sed('test_nlo_base-template.sin', replace_line=replace_func,
      new_file='test_nlo_scan-template.sin', write_to_top='#SETSCAN')
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_scan-template.sin'),
      True, "test_nlo_scan should work with purpose scan")

  proc_dict = {'purpose': 'nlo'}
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'),
      True, "test_nlo_base should work with purpose nlo")

  with open('test_nlo_resonances-template.sin', "w") as test:
    test.write('process test_nlo_resonances = e1, E1 => e2, E2' +
        ' {nlo_calculation = "Full"}\n' +
        '?fks_mapping_type = "resonances"\n')
  proc_dict = {'purpose': 'nlo'}
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_resonances-template.sin'), False)

  proc_dict = {'purpose': 'nlo', 'fks_method': 'resonances'}
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_resonances-template.sin'), True)

  os.remove('test_nlo_wrong.sin')
  os.remove('test_nlo_scan-template.sin')
  os.remove('test_nlo_resonances-template.sin')


def check_for_valid_wizard_sindarin(proc_dict, template_sindarin):
  if not is_valid_wizard_sindarin(proc_dict, template_sindarin):
    ut.fatal('Given sindarin (' + template_sindarin + ') is invalid for intended use')
    return FAIL
  return SUCCESS


@nt.with_setup(create_test_nlo_base, remove_test_nlo_base)
def test_check_for_valid_wizard_sindarin():
  proc_dict = {'purpose': 'foo'}
  nt.eq_(check_for_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'),
      SUCCESS)

  proc_dict = {'purpose': 'scan'}
  nt.eq_(check_for_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'),
      FAIL)


def create_scale_sindarins(base_sindarin, proc_dict):
  new_sindarins = []
  for suffix in get_scale_suffixes():
    new_sindarin = insert_suffix_in_sindarin(base_sindarin, suffix)
    new_sindarins.append(new_sindarin)
    shutil.copyfile(base_sindarin, new_sindarin)
    scale_multiplier = proc_dict.get('scale_multiplier', 2.0)
    if suffix == 'low':
      replace_scale(1.0 / scale_multiplier, new_sindarin)
    elif suffix == 'high':
      replace_scale(scale_multiplier, new_sindarin)
    replace_proc_id(suffix, new_sindarin)
  return new_sindarins


def multiply_sindarins(integration_sindarin, proc_dict, scaled, nlo_type,
    all_sindarins=''):
  scaled_sindarins = None
  if scaled:
    scaled_sindarins = create_scale_sindarins(integration_sindarin, proc_dict)
  if nlo_type == 'nlo':
    if scaled_sindarins is not None:
      for sindarin in scaled_sindarins:
        create_nlo_component_sindarins(proc_dict, sindarin)
    else:
      create_nlo_component_sindarins(proc_dict, integration_sindarin)


def replace_proc_id(part, filename):
  # Expects part  = 'Real', 'Born', etc as strings
  proc_id = ut.get_process(filename)
  replace_func = lambda l : l.replace(proc_id, proc_id + '_' + part)
  ut.sed(filename, replace_line=replace_func)


@nt.with_setup(create_test_nlo_base, remove_test_nlo_base)
def test_replace_proc_id():
  filename = 'test_replace_proc_id'
  shutil.copyfile('test_nlo_base-template.sin', filename)
  replace_proc_id('Real', filename)
  nt.eq_(ut.get_process(filename), 'test_nlo_base_Real')
  with open(filename, "r") as test:
    expectation = ['include("process_settings.sin")\n',
                   'process test_nlo_base_Real = e1, E1 => e2, E2 ' +
                   '{nlo_calculation = "Full"}\n',
                   'integrate (test_nlo_base_Real)']
    for t, e in zip(test, expectation):
      nt.eq_(t, e)
  os.remove(filename)


def replace_iterations(adaption_iterations, integration_iterations):
  iterations = 'iterations = ' + adaption_iterations + ':"gw"'
  if (integration_iterations != ' '):
    iterations += ',' + integration_iterations
  return lambda line: line.replace('#ITERATIONS', iterations)


def replacements(adaption_iterations, integration_iterations, process):
  replace_iters = replace_iterations(adaption_iterations,
      integration_iterations)
  replace_process = lambda line: line.replace('PROCESS', process)
  replace_line = lambda line: replace_process(replace_iters(line))
  return replace_line


def create_integration_sindarin(integration_sindarin, template_sindarin,
    process, adaption_iterations, integration_iterations):
  replace_line = replacements(adaption_iterations, integration_iterations,
      process)
  ut.sed(template_sindarin, replace_line, new_file=integration_sindarin)


@nt.with_setup(create_test_nlo_base, remove_test_nlo_base)
def test_create_integration_sindarin():
  with open('test_integration-template.sin', "w") as test:
    test.write('process PROCESS = e1, E1 => e2, E2 {#ITERATIONS} integrate (PROCESS)')
  create_integration_sindarin('test_integration.sin',
      'test_integration-template.sin', 'test_integration', "3:100", "1:500")
  with open('test_integration.sin', "r") as test:
    nt.eq_(test.read(), 'process test_integration = e1, E1 => e2, E2 ' +
        '{iterations = 3:100:"gw",1:500} integrate (test_integration)')
  os.remove('test_integration-template.sin')
  os.remove('test_integration.sin')


def create_simulation_sindarin(simulation_sindarin, template_sindarin, process,
    adaption_iterations, integration_iterations, n_events):
  replace_line = replacements(adaption_iterations, integration_iterations,
      process)
  ut.sed(template_sindarin, replace_line, new_file=simulation_sindarin)
  command = 'n_events = ' + str(n_events) + '\n' \
      + 'checkpoint = n_events / 20' + '\n' \
      + 'simulate(' + process + ')'
  ut.sed(simulation_sindarin, write_to_bottom=command)


def get_grid_index(proc_name, beam_type):
  words = proc_name.split('_')
  if beam_type == 'leptons':
     grid_indices = {'Born': 1, 'Real': 2, 'Virtual': 3, 'Mismatch': 4}
  else:
     grid_indices = {'Born': 1, 'Real': 2, 'Virtual': 3, 'Dglap': 4, 'Mismatch': 5}
  return grid_indices[words[-1]]


def test_get_grid_index():
  proc_name = 'proc_nlo_Born'
  nt.eq_(get_grid_index(proc_name, 'leptons'), 1)
  proc_name = 'proc_nlo_Real'
  nt.eq_(get_grid_index(proc_name, 'leptons'), 2)
  proc_name = 'proc_nlo_Virtual'
  nt.eq_(get_grid_index(proc_name, 'leptons'), 3)
  proc_name = 'proc_nlo_Mismatch'
  nt.eq_(get_grid_index(proc_name, 'leptons'), 4)


# TODO: (bcn 2016-03-30) review this
def divider(matchobj, batches):
  # nevents = matchobj.group(2)
  divided = str(int(float(matchobj.group(2)) / batches))
  return matchobj.group(1) + divided + matchobj.group(3)


events_re = re.compile(r"(n_events = )([0-9]*)( \* K)")


def set_seed(filename, samplename):
  seed = 'seed = ' + str(abs(hash(samplename)) % (10**8)) + '\n'
  ut.sed(filename, write_to_top=seed)


def change_sindarin_for_event_gen(filename, samplename, i, proc_dict):
  sample = '$sample = "' + samplename + '"\n'
  # seed = 'seed = ' + str(abs(hash(samplename)) % (10 ** 8)) + '\n'
  events_per_batch = proc_dict['events_per_batch']
  if events_per_batch is None:
    replace_func = partial(divider, batches=proc_dict['batches'])
  else:
    replace_func = lambda x : x.group(1) + str(events_per_batch)
  replace_line = lambda line : events_re.sub(
      replace_func, line).replace('include("', 'include("../')
  ut.sed(filename, replace_line, write_to_top=sample)
  set_seed(filename, samplename)


def run_json(json_name):
  run_json = retrieve_and_validate_run_json('tests', json_name=json_name)
  with ut.cd('tests'):
    setup_sindarins(run_json)
    whizard = Whizard(run_json, False)
    runs = fill_all_runs(run_json)
    return map(whizard.run_process, runs)


def clean_whizard_folder():
  cmd = "find . ! -name '*-template.sin' -type f -exec rm -f {} +"
  with ut.cd('tests/whizard'):
    return_code = subprocess.call(cmd, shell=True)
    nt.eq_(return_code, 0)


@nt.with_setup(clean_whizard_folder)
def test_integration_whizard_wizard_disabled():
  results = run_json('disabled.json')
  nt.eq_(results, [])


@nt.with_setup(clean_whizard_folder)
def test_integration_whizard_wizard_lo():
  results = run_json('lo.json')
  nt.eq_(results, [FAIL])


@nt.with_setup(clean_whizard_folder)
def test_integration_whizard_wizard_test_soft():
  results = run_json('test_soft.json')
  nt.eq_(results, [SUCCESS])


@nt.with_setup(clean_whizard_folder)
def test_integration_whizard_wizard_scan():
  results = run_json('scan.json')
  nt.ok_(all([r == SUCCESS for r in results]))


@nt.with_setup(clean_whizard_folder)
def test_integration_whizard_wizard_scan_WbWbH():
  results = run_json('WbWbH_scan.json')
  nt.ok_(all([r == SUCCESS for r in results]))
