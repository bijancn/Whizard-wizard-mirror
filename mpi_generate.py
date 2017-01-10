#!/usr/bin/env python
# Main program to generate results. To be run like in mpi_run_this.sh

import argparse
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

  # Parse command line options
  parser = argparse.ArgumentParser(description='Run the whizard wizard with mpi_map',
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('process_folder', help='The process folder to be run')

  # options how to behave
  parser.add_argument("-v", '--verbose', action='store_true',
      help='Show whizard output or not')

  args = parser.parse_args()

  run_json = whizard_wizard.retrieve_and_validate_run_json(args.process_folder)
  whizard_wizard.setup_sindarins(run_json)
else:
  run_json = None
  args = None
run_json = comm.bcast(run_json, root=0)
args = comm.bcast(args, root=0)
whizard = whizard_wizard.Whizard(run_json, args.verbose)

comm.Barrier()

runs = whizard_wizard.fill_all_runs(run_json)

results = mpi_map(whizard.run_process, runs)

if comm.Get_rank() == 0:
  logger.info('This is the MPI master: All processes returned.')
  for res, run in zip(results, runs):
    if res != whizard_wizard.SUCCESS:
      fatal('Unsuccessful run occured. Return code: ' + str(res) +
          ' in this run ' + str(run))
  logger.info("""
#==============================================================================#
#                                     DONE                                     #
#==============================================================================#
""")
