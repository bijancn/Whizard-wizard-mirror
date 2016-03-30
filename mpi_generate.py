#!/usr/bin/env python
import sys
from mpi4py_map import mpi_map, comm
import whizard_wizard
from utils import logger, fatal

if comm.Get_rank() == 0:
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
  run_json = whizard_wizard.retrieve_and_validate_run_json(process_folder)
  whizard_wizard.setup_sindarins(run_json)
else:
  run_json = None
run_json = comm.bcast(run_json, root=0)
whizard = whizard_wizard.Whizard(run_json)

comm.Barrier()

runs = whizard_wizard.fill_all_runs (run_json)

mpi_map(whizard.run_process, runs)

if comm.Get_rank() == 0:
  logger.info('This is the MPI master: All processes returned.')
  logger.info("""
#==============================================================================#
#                                     DONE                                     #
#==============================================================================#
""")
