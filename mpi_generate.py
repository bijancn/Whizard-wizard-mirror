#!/usr/bin/env python
from mpi4py_map import mpi_map, comm
from subproc import replace_file, whizard_run, fatal, run
from utils import cd, mkdirs
from numpy import arange
from mpi4py import MPI
import subprocess
import textwrap
import logging
import time
import shutil
import os
import sys
import json

def setup_logger():
  logPath = os.getcwd()
  logName = 'default'
  logFormatter = logging.Formatter('%(asctime)s ' + \
      '[%(levelname)-5.5s]  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
  rootLogger = logging.getLogger()
  fileHandler = logging.FileHandler('{0}/{1}.log'.format(logPath, logName))
  fileHandler.setFormatter(logFormatter)
  rootLogger.addHandler(fileHandler)
  rootLogger.setLevel(logging.INFO)
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(logFormatter)
  rootLogger.addHandler(consoleHandler)
  logger = logging.getLogger(__name__)
  return logger

def load_json():
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
  json_file = os.path.join(process_folder, 'local.json')
  logger.info('Trying to read: ' + json_file)
  try:
    with open(json_file) as f:
      json_info = json.load(f)
  except IOError:
    fatal('json not found. Either wrong process directory or missing local.json')
  except ValueError:
    fatal('json seems invalid. Check it on http://jsonlint.com/')
  logger.info('Found the following processes:')
  for p in json_info['processes']:
    logger.info(p['process'] + '\t[' + p['purpose'] + ']')
  return json_info

def log(action, batch, process):
  logger.info(textwrap.fill(action + ' batch ' + str(batch) + ' of '+ \
      str(process) + ' on ' + MPI.Get_processor_name()))

def setup_sindarins(process, batch=None):
  logger.info('Setting up sindarins of ', str(process))
  sindarin = process['process'] + '.sin'
  template_sindarin = sindarin.replace('.sin', '-template.sin')
  integration_sindarin = sindarin.replace('.sin', '-integrate.sin')
  template_present = os.path.isfile(template_sindarin)
  scan = process['purpose'] == 'scan'
  if scan and not template_present:
    logger.error('You have to give a template for a scan')
    sys.exit(1)
  elif not scan and not template_present:
    fallback = integration_sindarin + ' and ' + integration
    if os.path.isfile(integration_sindarin) and os.path.isfile(sindarin):
      logger.info('Didnt find a template, will use ' + fallback)
      return
    else:
      logger.error('Didnt find a template nor ' + fallback)
      sys.exit(1)
  if template_present:
    create_integration_sindarin(integration_sindarin, template_sindarin,
        process['adaption_iterations'], process['integration_iterations'])

def run_process((proc_id, process)):
  log('Running', proc_id, process)
  sindarin = process['process'] + '.sin'
  integration_sindarin = str(sindarin).replace('.sin', '-integrate.sin')
  integration_grids = str(sindarin).replace('.sin', '_m1.vg')
  directory = 'whizard/'
  with cd(directory):
    if not os.path.exists(integration_grids) and \
        (process['purpose'] == 'events' or process['purpose'] == 'histograms'):
      logger.error('Didnt find integration grids but you wanted events! ' + \
          'Aborting! Please use "integrate" first')
      return
    elif process['purpose'] == 'integrate':
      logger.info('Generating the following integration grids: ' + integration_grids)
      whizard_run(whizard=whizard,
          core=comm.Get_rank(),
          sindarin=integration_sindarin,
          options=process['whizard_options'])
    else:
      logger.info('Using the following integration grids: ' + integration_grids)
      runfolder = process['process'] + '-' + str(proc_id)
      if (not os.path.isfile(os.path.join(runfolder, 'done'))):
        run(proc_id,
            purpose=process['purpose'],
            whizard=whizard,
            sindarin=sindarin,
            integration_grids=integration_grids,
            batches=process['batches'],
            options=process['whizard_options'],
            events_per_batch=process['events_per_batch'],
            analysis=json_info['analysis'])
        if (os.path.isfile(os.path.join(runfolder, 'done') and \
            process['purpose'] == 'events')):
          os.rename(os.path.join(runfolder, runfolder) + '.hepmc',
              os.path.join("../rivet", runfolder + '.hepmc'))
      else:
        logger.info('Skipping ' + runfolder)

logger = setup_logger ()
if comm.Get_rank() == 0:
  json_info = load_json()
  for p in json_info['processes']:
    setup_sindarins(p)
else:
  json_info = None
json_info = comm.bcast(json_info, root=0)
whizard = json_info['whizard']
  # TODO: (bcn 2016-02-25) make this check or search for the executable
  # if not os.path.exists(whizard):
    # print 'No valid whizard binary'
    # print 'whizard = ', whizard
    # sys.exit(1)

comm.Barrier()

runs = []
for p in json_info['processes']:
  if p['purpose'] == 'events':
    runs += [(b, p) for b in range(p['batches'])]
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
