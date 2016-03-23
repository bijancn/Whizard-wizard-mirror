#!/usr/bin/env python
from mpi4py_map import mpi_map, comm
import subproc
from utils import cd, fatal, load_json, setup_logger
import jsonschema
from distutils import spawn
from mpi4py import MPI
import subprocess
import textwrap
import logging
import time
import shutil
import os
import sys
from termcolor import colored


def mpi_load_json():
  logger.info("""
#==============================================================================#
#                                   NEW RUN                                    #
#==============================================================================#
""")
  logger.info('This is the MPI master in the initializing phase')
  logger.info('Total number of available cores: %g', comm.Get_size())
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
          subproc.create_integration_sindarin(integration_sindarin, template_sindarin,
              proc_dict['adaption_iterations'], proc_dict.get('integration_iterations', ' '))
          subproc.multiply_sindarins (integration_sindarin, proc_dict, 
             proc_dict.get('scale_variation', False), proc_dict['nlo_type'])
          #scaled_sindarins = None
          #if proc_dict.get('scale_variation', False):
          #  scaled_sindarins = subproc.create_scale_sindarins (integration_sindarin)
          #if proc_dict['nlo_type'] == 'nlo':
          #  if scaled_sindarins != None:
          #    for sindarin in scaled_sindarins:
          #      subproc.create_nlo_component_sindarins(sindarin)
          #  else:
          #    subproc.create_nlo_component_sindarins(integration_sindarin)
        elif proc_dict['purpose'] == 'histograms' or proc_dict['purpose'] == 'events':
          subproc.create_simulation_sindarin(base_sindarin, template_sindarin,
              proc_dict['process'], proc_dict['adaption_iterations'], 
              proc_dict.get('integration_iterations', ' '), 
              proc_dict['events_per_batch']) 
          subproc.multiply_sindarins (base_sindarin, proc_dict,  
             proc_dict.get('scale_variation', False), proc_dict['nlo_type'])
          ### Evil code duplication
          #scaled_sindarins = None
          #if proc_dict.get('scale_variation', False):
          #  scaled_sindarins = subproc.create_scale_sindarins (base_sindarin)
          #if proc_dict['nlo_type'] == 'nlo':
          #  if scaled_sindarins != None:
          #    for sindarin in scaled_sindarins:
          #      subproc.create_nlo_component_sindarins(sindarin)
          #  else:
          #    subproc.create_nlo_component_sindarins(base_sindarin)

  else:
    logger.info('Skipping ' + proc_dict['process'] + ' because it is disabled')

def run_process((proc_id, proc_name, proc_dict)):
  log('Running', proc_id, proc_dict)
  integration_sindarin = proc_name + '-integrate.sin'
  if proc_dict['nlo_type'] == 'nlo':
    integration_grids = proc_name + '_m' + str (subproc.get_grid_index(proc_name)) + '.vg'
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
      subproc.whizard_run(purpose, whizard,
          proc_id=comm.Get_rank(),
          sindarin=integration_sindarin,
          options=whizard_options)
    else:
      if event_generation:
        logger.info('Using the following integration grids: ' + integration_grids)
      runfolder = proc_name + '-' + str(proc_id)
      if (not os.path.isfile(os.path.join(runfolder, 'done'))):
        analysis = proc_dict.get('analysis', '')
        subproc.generate(proc_name,
            proc_id,
            proc_dict,
            whizard=whizard,
            integration_grids=integration_grids,
            analysis=analysis)
        if (os.path.isfile(os.path.join(runfolder, 'done')) and \
            purpose == 'events'):
          os.rename(os.path.join(runfolder, runfolder) + '.hepmc',
              os.path.join("../rivet", runfolder + '.hepmc'))
        return
      else:
        logger.info('Skipping ' + runfolder + ' because done is found')

logger = setup_logger ()
if comm.Get_rank() == 0:
  run_json = mpi_load_json()
  for p in run_json['processes']:
    setup_sindarins(p)
else:
  run_json = None
run_json = comm.bcast(run_json, root=0)
whizard = run_json['whizard']
if not spawn.find_executable(whizard):
  fatal('No valid whizard found. You gave whizard = ' + whizard)
else:
  logger.info('Using ' + whizard)

comm.Barrier()

runs = []
for proc_dict in run_json['processes']:
  template = proc_dict['process'] + '-template'
  if proc_dict.get ('scale_variation', False):
    processes = subproc.append_scale_suffixes (proc_dict['process'])
  else:
    processes = [proc_dict['process']]
  for proc_name in processes:
    if proc_dict['nlo_type'] == 'nlo':
      for nlo_proc_name in subproc.create_component_sindarin_names (proc_name, proc_dict):
        runs += subproc.fill_runs(nlo_proc_name, proc_dict)
    else:
      runs += subproc.fill_runs(proc_name, proc_dict)

mpi_map(run_process, runs)

if comm.Get_rank() == 0:
  logger.info('This is the MPI master: All processes returned.')
  logger.info("""
#==============================================================================#
#                                     DONE                                     #
#==============================================================================#
""")
