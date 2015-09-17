#!/usr/bin/env python

import logging
import logging.config
import sys
import os
import multiprocessing as mp
import imp
from functools import partial
from numpy import arange

from subproc import run, parser, jobs

if __name__ == '__main__':
  args = parser.parse_args()
  start = int(args.start)
  end = int(args.end)
  if args.stepsize is None:
    stepsize = 1
  else:
    stepsize = args.stepsize
  range_ = list(arange(start, end, stepsize))
  this_run = partial(run, args=args)
  pool = mp.Pool(processes=jobs)
  print range_
  print args
  results = pool.map(this_run, range_)
