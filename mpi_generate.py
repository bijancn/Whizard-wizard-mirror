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

# TODO: (bcn 2016-02-25) should be generated automagically
# TODO: (bcn 2016-02-25) use adaption_iterations
# TODO: (bcn 2016-02-25) use integration_iterations
def setup_sindarins(p):
  logger.info( 'Setting up sindarins for ' + p['process'])
  return

def run_process((proc_id, process)):
  print ('in run process') ### Debugging
  logger.info(textwrap.fill('Running batch ' + str(proc_id) + ' of '+ \
      str(process) + ' on ' + MPI.Get_processor_name()))
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
