import logging
import logging.config
import sys
import os
import multiprocessing as mp
import yaml
from functools import partial

from utils import cd
from subproc import batches, whizard_run, run

logger = logging.getLogger(__name__)
jobs = 10

if __name__ == '__main__':
  path = 'logging.yaml'
  if os.path.exists(path):
    with open(path, 'rt') as f:
      config = yaml.load(f.read())
      logging.config.dictConfig(config)

  logger.info("""
#==============================================================================#
#                                   NEW RUN                                    #
#==============================================================================#
""")

  whizard = sys.argv[1]
  sindarin = sys.argv[2]
  directory = 'whizard/'
  sindarin = sindarin.replace(directory, '')

  with cd(directory):
    integration_sindarin = str(sindarin).replace('.sin', '-integrate.sin')
    integration_grids = str(sindarin).replace('.sin', '_m1.vg')
    if not os.path.exists(integration_grids):
      logger.info('Didnt find integration grids')
      whizard_run(whizard, integration_sindarin)
    else:
      logger.info('Using the following integration grids: ' + integration_grids)
    this_run = partial(run, whizard=whizard, sindarin=sindarin,
        integration_grids=integration_grids)
    pool = mp.Pool(processes=jobs)
    #results = pool.map_async(this_run, range(batches)) #.get(9999999)
    results = pool.map(this_run, range(batches)) #.get(9999999)

  logger.info("""
#==============================================================================#
#                                     DONE                                     #
#==============================================================================#
""")
