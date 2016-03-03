#!/usr/bin/env python
from mpi4py_map import mpi_map, comm
import subproc
from utils import cd, fatal, load_json, setup_logger
from numpy import arange
from mpi4py import MPI
import subprocess
import textwrap
import logging
import time
import shutil
import os
import sys
import numpy as np

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
  logger.info('Trying to read: ' + json_file)
  run_json = load_json(json_file)
  logger.info('Found the following processes:')
  for p in run_json['processes']:
    logger.info(p['process'] + '\t[' + p['purpose'] + ']')
  return run_json

def log(action, batch, proc_dict):
  logger.info(textwrap.fill(action + ' batch ' + str(batch) + ' of '+ \
      str(proc_dict) + ' on ' + MPI.Get_processor_name()))

def setup_sindarins(proc_dict, batch=None):
  logger.info('Setting up sindarins of ' + str(proc_dict))
  with cd('whizard/'):
    sindarin = proc_dict['process'] + '.sin'
    template_sindarin = sindarin.replace('.sin', '-template.sin')
    integration_sindarin = sindarin.replace('.sin', '-integrate.sin')
    template_present = os.path.isfile(template_sindarin)
    scan = proc_dict['purpose'] == 'scan'
    if scan and not template_present:
      logger.error('You have to supply ' + template_sindarin + ' for a scan')
      sys.exit(1)
    elif not scan and not template_present:
      fallback = integration_sindarin + ' and ' + sindarin
      if os.path.isfile(integration_sindarin) and os.path.isfile(sindarin):
        logger.info('Didnt find ' + template_sindarin + ', will use ' + fallback)
        return
      else:
        logger.error('Didnt find ' + template_sindarin + ' nor ' + fallback)
        sys.exit(1)
    if template_present:
      subproc.create_integration_sindarin(integration_sindarin, template_sindarin,
          proc_dict['adaption_iterations'], proc_dict['integration_iterations'])

def run_process((proc_id, proc_dict)):
  log('Running', proc_id, proc_dict)
  integration_sindarin = proc_dict['process'] + '-integrate.sin'
  integration_grids = proc_dict['process'] + '_m1.vg'
  purpose = proc_dict['purpose']
  event_generation = purpose == 'events' or purpose == 'histograms'
  with cd('whizard/'):
    if not os.path.exists(integration_grids) and event_generation:
      logger.error('Didnt find integration grids but you wanted events! ' + \
          'Aborting! Please use "integrate" first')
      return
    elif purpose == 'integrate':
      logger.info('Generating the following integration grids: ' + integration_grids)
      subproc.whizard_run(purpose, whizard,
          proc_id=comm.Get_rank(),
          sindarin=integration_sindarin,
          options=proc_dict['whizard_options'])
    else:
      if event_generation:
        logger.info('Using the following integration grids: ' + integration_grids)
      runfolder = proc_dict['process'] + '-' + str(proc_id)
      if (not os.path.isfile(os.path.join(runfolder, 'done'))):
        try:
          analysis = run_json['analysis']
        except KeyError:
          analysis = ''
        subproc.generate(proc_id,
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
        logger.info('Skipping ' + runfolder)

logger = setup_logger ()
if comm.Get_rank() == 0:
  run_json = mpi_load_json()
  for p in run_json['processes']:
    setup_sindarins(p)
else:
  run_json = None
run_json = comm.bcast(run_json, root=0)
whizard = run_json['whizard']
# TODO: (bcn 2016-02-25) make this check or search for the executable
# if not os.path.exists(whizard):
  # print 'No valid whizard binary'
  # print 'whizard = ', whizard
  # sys.exit(1)

comm.Barrier()

runs = []
for p in run_json['processes']:
  if p['purpose'] == 'events' or p['purpose'] == 'histograms':
    runs += [(b, p) for b in range(p['batches'])]
  elif p['purpose'] == 'scan':
    runs += [(b, p) for b in np.arange(float(p['start']), float(p['stop']),
      float(p['stepsize']))]
  elif p['purpose'] == 'integrate':
    runs += [(-1, p)]
mpi_map(run_process, runs)

if comm.Get_rank() == 0:
  logger.info('This is the MPI master: All processes returned sucessfully')
  logger.info("""
#==============================================================================#
#                                     DONE                                     #
#==============================================================================#
""")
