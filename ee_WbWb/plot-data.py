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
  return None

def pretty_label(l, title):
  l = os.path.basename(l)
  l = l.replace('proc', '')
  l = l.replace('_thresholdparams', '')
  l = l.replace('_lo', '')
  if not 'ttbar' in l:
    l = '$W^+b W^-\\bar b$, ' + l
  else:
    l = l.replace('ttbar_lo_thresholdparams', '$t \\bar t$')
  l = l.replace('.dat', '')
  l = l.replace('_', ', ')
  l = l.replace(', , ', ', ')
  l = re.sub(r", $", "", l)
  l = l.replace(', , ', ', ')
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
