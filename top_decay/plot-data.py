#!/usr/bin/env python
import sys
import os
import glob
import re
import multiprocessing as mp
import numpy as np
import inspect
from functools import partial
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import bcn_plot
from utils import load_json

def ls_decider(lbl, title):
  if 'proc_lo' in lbl:
    return 'dashed'
  else:
    return 'solid'

def pretty_label(l, title):
  l = os.path.basename(l)
  l = l.replace('proc_lo', 'LO')
  l = l.replace('proc_nlo', 'NLO')
  l = l.replace('.dat', '')
  return l

def main ():
  pic_path = os.path.abspath('./plots') + '/'
  data_path = os.path.abspath('./scan-results')
  files = glob.glob(data_path + '/*.dat')
  plot_json = load_json('plot.json')
  data = [(filename, np.loadtxt(filename, unpack=True)) for filename in files]
  pool = mp.Pool(processes=3)
  plot_this = partial(bcn_plot.plot, data=data, pic_path=pic_path,
      linestyle_decider=ls_decider, pretty_label=pretty_label)
  pool.map(plot_this, plot_json['plots'])

main()
