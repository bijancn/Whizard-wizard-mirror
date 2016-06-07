#!/usr/bin/env python
import sys
import os
import glob
import re
import multiprocessing as mp
import inspect
from functools import partial
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import bcn_plot
import data_utils
from utils import load_json

parallel = False


def ls_decider(lbl, title):
  if 'soft limit' in title and 'scatter' in title:
    return 'scatter'
  elif 'soft limit' in title and 'histogram' in title:
    return 'histogram'
  elif 'production' in lbl:
    return 'dashed'
  elif 'decay' in lbl:
    return 'dashdot'
  elif 'Gauge-dependence' in title:
    return 'banded'
  elif 'onshell projections' in title:
    return 'solid'
  elif 'central' in lbl:
    return 'solid'
  else:
    return None


def pretty_label(filename, title):
  l = os.path.basename(filename)
  l = l.replace('proc', '')
  l = l.replace('_thresholdparams', '')
  l = l.replace('_lo', '')
  if 'ttbar' not in l:
    l = '$W^+b W^-\\bar b$, ' + l
  else:
    l = l.replace('ttbar_lo_thresholdparams', '$t \\bar t$')
  l = l.replace('.dat', '')
  l = l.replace('_', ', ')
  l = l.replace(', , ', ', ')
  l = re.sub(r", $", "", l)
  l = l.replace(', , ', ', ')
  l = l.replace('productiononshellprojected',
      'only for $\\mathcal{M}^{\\text{production}}$ projected')
  l = l.replace('decayonshellprojected',
      'only for $\\mathcal{M}^{\\text{decay}}$ projected')
  l = l.replace('fact', 'factorized')
  l = l.replace('onshellprojected', 'onshell projected')
  l = l.replace('widthunprojected', '$\\Gamma[\\sqrt{p--{\\text{top}}^2}]$')
  l = l.replace('ttbar', '$t \\bar t$')
  return l


def main():
  print 'Start'
  pic_path = os.path.abspath('./plots') + '/'
  data_path = os.path.abspath('./scan-results')
  data_path2 = os.path.abspath('../ee_tt/scan-results')
  files = glob.glob(data_path + '/*.dat')
  files += glob.glob(data_path2 + '/*.dat')
  data = data_utils.load_and_clean_files(files)
  plot_this = partial(bcn_plot.plot, data=data, pic_path=pic_path,
      linestyle_decider=ls_decider, pretty_label=pretty_label)
  plot_json = load_json('plot.json')
  if parallel:
    pool = mp.Pool(processes=4)
    pool.map(plot_this, plot_json['plots'])
  else:
    map(plot_this, plot_json['plots'])

main()
