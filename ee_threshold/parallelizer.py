import logging
import logging.config
import sys
import os
import multiprocessing as mp
import imp
from functools import partial

from utils import cd
from subproc import jobs, batches, whizard_run, run

if __name__ == '__main__':
  folder = sys.argv[1]
  start = int(sys.argv[2])
  end = int(sys.argv[3])
  this_run = partial(run, folder=folder)
  pool = mp.Pool(processes=jobs)
  print range(start,end)
  results = pool.map(this_run, range(start,end))
