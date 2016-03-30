#!/usr/bin/env python
from mpi4py_map import mpi_map, comm
import subproc
from utils import logger

if comm.Get_rank() == 0:
  logger.info("""
#==============================================================================#
#                                   NEW RUN                                    #
#==============================================================================#
""")
  logger.info('This is the MPI master in the initializing phase')
  logger.info('Total number of available cores: %g', comm.Get_size())
  run_json = subproc.mpi_load_json()
  for p in run_json['processes']:
    subproc.setup_sindarins(p)
else:
  run_json = None
run_json = comm.bcast(run_json, root=0)
whizard = subproc.Whizard(run_json)

comm.Barrier()

runs = subproc.fill_all_runs (run_json)

mpi_map(whizard.run_process, runs)

if comm.Get_rank() == 0:
  logger.info('This is the MPI master: All processes returned.')
  logger.info("""
#==============================================================================#
#                                     DONE                                     #
#==============================================================================#
""")
