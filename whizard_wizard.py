import os
import re
import shutil
import subprocess
import textwrap
# import unittest   # has decorator for skipping tests: @unittest.skip("reason")
from distutils import spawn
from functools import partial
import jsonschema
from mpi4py import MPI
from numpy import logspace, arange
import nose.tools as nt
import utils as ut
# from termcolor import colored


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
  ut.logger.info('Found the following processes:')
  for p in json['processes']:
    ut.logger.info(p['process'] + '\t[' + p['purpose'] + ']')
  return json


def log(action, batch, proc_dict):
  ut.logger.info(textwrap.fill(action + ' batch ' + str(batch) + ' of ' +
      str(proc_dict) + ' on ' + MPI.Get_processor_name()))


# TODO: (bcn 2016-03-30) slim the Whizard. would be nice to only have
# information and data how to run Whizard here
SUCCESS, FAIL = range(2)


class Whizard():
  def __init__(self, run_json):
    self.binary = run_json['whizard']
    if not spawn.find_executable(self.binary):
      ut.fatal('No valid whizard found. You gave whizard = ' + self.binary)
    else:
      ut.logger.info('Using ' + self.binary)

  def execute(self, purpose, sindarin, fifo=None, proc_id=None, options='',
      analysis=''):
    cmd = self.binary + ' ' + sindarin + ' ' + options
    if (purpose == 'histograms'):
      cmd = 'export RIVET_ANALYSIS_PATH=../../rivet; ' + cmd
      yoda_file = '../../rivet/' + fifo.replace('hepmc', 'yoda')
      cmd = cmd + ' & rivet --quiet -H ' + yoda_file + ' -a ' + analysis + ' ' + fifo
    num = ' in ' + str(proc_id) if proc_id is not None else ''
    ut.logger.info('Calling subprocess ' + cmd + num)
    try:
      return_code = subprocess.call(cmd, shell=True)
    except Exception as e:
      ut.fatal('Exception occured: ' + str(e) + 'Whizard failed on executing ' +
          sindarin + num)
      return FAIL
    else:
      if not ut.grep('ERROR', 'whizard.log'):
        ut.logger.info('Whizard finished' + num)
        with open('done', 'a'):
          os.utime('done', None)
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
    ut.mkdirs(runfolder)
    if event_generation:
      shutil.copyfile(sindarin, os.path.join(runfolder, sindarin))
      shutil.copyfile(integration_grids, os.path.join(runfolder, integration_grids))
      with ut.cd(runfolder):
        if (purpose == 'histograms'):
          ut.remove(fifo)
          subprocess.call("mkfifo " + fifo, shell=True)
        change_sindarin_for_event_gen(sindarin, runfolder, proc_id, proc_dict)
        return self.execute(purpose, sindarin, fifo=fifo, proc_id=proc_id,
            options=options, analysis=analysis)
    elif purpose == 'scan':
      scan_expression = proc_dict['scan_object'] + " = " + str(proc_id)
      replace_line = lambda line: line.replace('#SETSCAN',
        scan_expression).replace('include("', 'include("../')
      integration_sindarin = proc_name + '-integrate.sin'
      ut.sed(integration_sindarin, replace_line,
          new_file=os.path.join(runfolder, sindarin))
      with ut.cd(runfolder):
        return self.execute(purpose, sindarin, proc_id=proc_id, options=options)
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
        return self.execute(purpose, sindarin, proc_id=proc_id, options=options)
    else:
      raise NotImplementedError

  def run_process(self, (proc_id, proc_name, proc_dict)):
    log('Trying', proc_id, proc_dict)
    integration_sindarin = proc_name + '-integrate.sin'
    if proc_dict['nlo_type'] == 'nlo':
      integration_grids = proc_name + '_m' + str(get_grid_index(proc_name)) + '.vg'
    else:
      integration_grids = proc_name + '_m1.vg'
    purpose = proc_dict['purpose']
    event_generation = purpose == 'events' or purpose == 'histograms'
    whizard_options = proc_dict.get('whizard_options', '--no-banner')
    with ut.cd('whizard/'):
      if not os.path.exists(integration_grids) and event_generation:
        ut.logger.error('Didnt find integration grids with name ' + integration_grids +
             ', but you wanted events! Aborting! Please use "integrate" first')
        return FAIL
      elif purpose == 'integrate':
        ut.logger.info('Generating the following integration grids: ' +
            integration_grids)
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
            done = os.path.isfile(os.path.join(runfolder, 'done'))
            if (done and purpose == 'events'):
              os.rename(os.path.join(runfolder, runfolder) + '.hepmc',
                  os.path.join("../rivet", runfolder + '.hepmc'))
            if (done and purpose == 'test_soft'):
              ut.mkdirs("../scan-results")
              os.rename(os.path.join(runfolder, 'soft.log'),
                  os.path.join("../scan-results", runfolder.strip('--1') + '.soft.dat'))
          return return_code
        else:
          ut.logger.info('Skipping ' + runfolder + ' because done is found')
          return SUCCESS


def setup_sindarins(run_json):
  for p in run_json['processes']:
    setup_sindarin(p)


def setup_sindarin(proc_dict):
  if proc_dict['purpose'] != 'disabled':
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
        if proc_dict['purpose'] == 'integrate' or scan or test_soft:
          create_integration_sindarin(integration_sindarin, template_sindarin,
              proc_dict['adaption_iterations'],
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


def setup_func():
  with open('test_nlo_base-template.sin', "w") as test:
    test.write('include("process_settings.sin")\n')
    test.write('process test_nlo_base = e1, E1 => e2, E2 {nlo_calculation = "Full"}\n')
    test.write('integrate (test_nlo_base)')


def teardown_func():
  os.remove('test_nlo_base-template.sin')


def fill_runs(proc_name, proc_dict):
  purpose = proc_dict['purpose']
  if purpose == 'events' or purpose == 'histograms':
    runs = [(b, proc_name, proc_dict) for b in range(proc_dict['batches'])]
  elif purpose == 'scan':
    try:
      start = float(proc_dict['start'])
      stop = float(proc_dict['stop'])
      stepsize = proc_dict['stepsize']
    # TODO: (bcn 2016-03-30) this should be made impossible in the scheme
    except KeyError:
      ut.fatal('Aborting: You want a scan but have not set start, stop and stepsize')
    else:
      if stepsize == 'logarithmic':
        step_range = logspace(start, stop, num=proc_dict.get('steps', 10),
            endpoint=True, base=10.0)
      else:
        step_range = arange(start, stop, float(stepsize))
      runs = [(b, proc_name, proc_dict) for b in step_range]
  elif purpose == 'integrate' or purpose == 'test_soft':
    runs = [(-1, proc_name, proc_dict)]
  elif purpose == 'disabled':
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
  nt.eq_(runs, [(0, proc_name, proc_dict), (1, proc_name, proc_dict)])

  proc_dict = {'purpose': 'scan', 'start': 0.1, 'stop': 0.2, 'stepsize': 0.05}
  runs = fill_runs(proc_name, proc_dict)
  expectation = [(0.1, proc_name, proc_dict), (0.15, proc_name, proc_dict)]
  for r, e in zip(runs, expectation):
    nt.assert_almost_equal(r[0], e[0], places=4)
    nt.eq_(r[1:2], e[1:2])

  proc_dict = {'purpose': 'integrate'}
  runs = fill_runs(proc_name, proc_dict)
  nt.eq_(runs, [(-1, proc_name, proc_dict)])

  proc_dict = {'purpose': 'disabled'}
  runs = fill_runs(proc_name, proc_dict)
  nt.eq_(runs, [])

  proc_dict = {'purpose': 'scan', 'start': 1, 'stop': 2,
      'stepsize': 'logarithmic', 'steps': 1}
  runs = fill_runs(proc_name, proc_dict)
  expectation = [(10, proc_name, proc_dict)]
  for r, e in zip(runs, expectation):
    nt.assert_almost_equal(r[0], e[0], places=4)
    nt.eq_(r[1:2], e[1:2])


@nt.raises(Exception)
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
  return suffixes


def get_scale_suffixes():
  return ['central', 'low', 'high']


def append_scale_suffixes(proc_name):
  return [proc_name + '_' + s for s in get_scale_suffixes()]


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


# TODO: (bcn 2016-03-29) is this used anywhere??? whats the purpose?
def get_full_proc_names(base_name, proc_dict):  # pragma: no cover
  scaled = proc_dict.get('scale_variation', False)
  nlo = proc_dict['nlo_type'] == 'nlo'
  if not scaled and not nlo:
    full_names = [base_name]
  else:
    if scaled:
      scaled_names = []
      for suffix in get_scale_suffixes():
        scaled_names += [base_name + '_' + suffix]
    else:
      scaled_names = [base_name]
    if nlo:
      full_names = []
      for scaled_name in scaled_names:
          full_names += create_nlo_component_names(scaled_name, proc_dict)
    else:
      full_names = scaled_names
  return full_names


def test_get_full_proc_names():
  pass


def is_nlo_calculation(filename):
  return ut.grep("nlo_calculation *=", filename)


@nt.with_setup(setup_func, teardown_func)
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


def create_nlo_component_sindarins(proc_dict, integration_sindarin):
  for suffix in get_component_suffixes(proc_dict):
    new_sindarin = insert_suffix_in_sindarin(integration_sindarin, suffix)
    shutil.copyfile(integration_sindarin, new_sindarin)
    replace_nlo_calc(suffix, new_sindarin)
    replace_proc_id(suffix, new_sindarin)


@nt.with_setup(setup_func, teardown_func)
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
  proc_id = ut.get_process(template_sindarin)
  valid = proc_id == template_sindarin.replace('-template.sin', '')
  purpose = proc_dict['purpose']
  if purpose == 'scan':
    valid = valid and ut.grep('#SETSCAN', template_sindarin)
  elif purpose == 'nlo' or purpose == 'nlo_combined':
    valid = valid and is_nlo_calculation(template_sindarin)
  return valid


@nt.with_setup(setup_func, teardown_func)
def test_is_valid_wizard_sindarin():
  proc_dict = {'purpose': 'foo'}
  with open('test_nlo_wrong.sin', "w") as test:
    test.write('process proc_nlo = e1, E1 => e2, E2 {nlo_calculation = "Full"}\n')
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_wrong.sin'), False)

  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'), True)

  proc_dict = {'purpose': 'scan'}
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'), False)

  replace_func = lambda l : l.replace('test_nlo_base', 'test_nlo_scan')
  ut.sed('test_nlo_base-template.sin', replace_line=replace_func,
      new_file='test_nlo_scan-template.sin', write_to_top='#SETSCAN')
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_scan-template.sin'), True)

  proc_dict = {'purpose': 'nlo'}
  nt.eq_(is_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin'), True)

  os.remove('test_nlo_wrong.sin')
  os.remove('test_nlo_scan-template.sin')


def check_for_valid_wizard_sindarin(proc_dict, template_sindarin):
  if not is_valid_wizard_sindarin(proc_dict, template_sindarin):
    ut.fatal('Given sindarin is invalid for intended use')


# TODO: (bcn 2016-03-30) this only executes but doesnt check.. maybe we can use raise?
def test_check_for_valid_wizard_sindarin():
  proc_dict = {'purpose': 'foo'}
  check_for_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin')

  proc_dict = {'purpose': 'scan'}
  check_for_valid_wizard_sindarin(proc_dict, 'test_nlo_base-template.sin')


def create_scale_sindarins(base_sindarin):
  new_sindarins = []
  for suffix in get_scale_suffixes():
    new_sindarin = insert_suffix_in_sindarin(base_sindarin, suffix)
    new_sindarins.append(new_sindarin)
    shutil.copyfile(base_sindarin, new_sindarin)
    if suffix == 'low':
      replace_scale(0.5, new_sindarin)
    elif suffix == 'high':
      replace_scale(2.0, new_sindarin)
    replace_proc_id(suffix, new_sindarin)
  return new_sindarins


def multiply_sindarins(integration_sindarin, proc_dict, scaled, nlo_type):
  scaled_sindarins = None
  if scaled:
    scaled_sindarins = create_scale_sindarins(integration_sindarin)
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


@nt.with_setup(setup_func, teardown_func)
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


def create_integration_sindarin(integration_sindarin, template_sindarin,
    adaption_iterations, integration_iterations):
  replace_line = replace_iterations(adaption_iterations, integration_iterations)
  ut.sed(template_sindarin, replace_line, new_file=integration_sindarin)


def create_simulation_sindarin(simulation_sindarin, template_sindarin, process,
    adaption_iterations, integration_iterations, n_events):
  replace_line = replace_iterations(adaption_iterations, integration_iterations)
  ut.sed(template_sindarin, replace_line, new_file=simulation_sindarin)
  command = 'n_events = ' + str(n_events) + '\n' \
      + 'checkpoint = n_events / 20' + '\n' \
      + 'simulate(' + process + ')'
  ut.sed(simulation_sindarin, write_to_bottom=command)


def get_grid_index(proc_name):
  words = proc_name.split('_')
  grid_indices = {'Born': 1, 'Real': 2, 'Virtual': 3, 'Mismatch': 4}
  return grid_indices[words[len(words) - 1]]


# TODO: (bcn 2016-03-30) review this
def divider(matchobj, batches):
  # nevents = matchobj.group(2)
  divided = str(int(float(matchobj.group(2)) / batches))
  return matchobj.group(1) + divided + matchobj.group(3)


events_re = re.compile(r"(n_events = )([0-9]*)( \* K)")


def change_sindarin_for_event_gen(filename, samplename, i, proc_dict):
  sample = '$sample = "' + samplename + '"\n'
  seed = 'seed = ' + str(abs(hash(samplename)) % (10 ** 8)) + '\n'
  events_per_batch = proc_dict['events_per_batch']
  if events_per_batch is None:
    replace_func = partial(divider, batches=proc_dict['batches'])
  else:
    replace_func = lambda x : x.group(1) + str(events_per_batch)
  replace_line = lambda line : events_re.sub(
      replace_func, line).replace('include("', 'include("../')
  ut.sed(filename, replace_line, write_to_top=sample + seed)


def run_json(json_name):
  run_json = retrieve_and_validate_run_json('tests', json_name=json_name)
  with ut.cd('tests'):
    setup_sindarins(run_json)
    whizard = Whizard(run_json)
    runs = fill_all_runs(run_json)
    return map(whizard.run_process, runs)


def clean_whizard_folder():
  cmd = "find . ! -name '*-template.sin' -type f -exec rm -f {} +"
  with ut.cd('tests/whizard'):
    return_code = subprocess.call(cmd, shell=True)
    nt.eq_(return_code, 0)


@nt.with_setup(setup=clean_whizard_folder)
def test_integration_whizard_wizard_1():
  results = run_json('disabled.json')
  nt.eq_(results, [])


@nt.with_setup(setup=clean_whizard_folder)
def test_integration_whizard_wizard_2():
  results = run_json('lo.json')
  nt.eq_(results, [FAIL])


@nt.with_setup(setup=clean_whizard_folder)
def test_integration_whizard_wizard_3():
  results = run_json('test_soft.json')
  nt.eq_(results, [SUCCESS])