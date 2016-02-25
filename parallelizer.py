import logging
import logging.config
import sys
import os
import multiprocessing as mp
import imp
from functools import partial

from utils import cd
from subproc import batches, whizard_run, run
jobs = int(os.getenv('WHIZARD_THREADS', 16))

try:
  imp.find_module('yaml')
  have_yaml = True
except ImportError:
  have_yaml = False
if have_yaml:
  import yaml

logger = logging.getLogger(__name__)

if __name__ == '__main__':
  path = 'logging.yaml'
  if os.path.exists(path) and have_yaml:
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
  if not os.path.exists(whizard):
    print 'No valid whizard binary'
    print 'whizard = ', whizard
    sys.exit(1)

  with cd(directory):
    integration_sindarin = str(sindarin).replace('.sin', '-integrate.sin')
    integration_grids = str(sindarin).replace('.sin', '_m1.vg')
    print 'integration_sindarin = ', integration_sindarin
    if not os.path.exists(integration_grids):
      logger.info('Didnt find integration grids')
      whizard_run(whizard, integration_sindarin)
    else:
      logger.info('Using the following integration grids: ' + integration_grids)
    this_run = partial(run, whizard=whizard, sindarin=sindarin,
        integration_grids=integration_grids)
    pool = mp.Pool(processes=jobs)
    #results = pool.map_async(this_run, range(batches)) #.get(9999999)
    results = pool.map(this_run, range(batches))

  logger.info("""
#==============================================================================#
#                                     DONE                                     #
#==============================================================================#
""")
