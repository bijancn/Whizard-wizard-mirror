import logging
import logging.config
import sys
import os
import multiprocessing as mp
import imp
from functools import partial

from subproc import run, parser, jobs

if __name__ == '__main__':
  args = parser.parse_args()
  start = int(args.start)
  end = int(args.end)
  this_run = partial(run, args=args)
  pool = mp.Pool(processes=jobs)
  print range(start, end)
  print args
  results = pool.map(this_run, range(start, end))
