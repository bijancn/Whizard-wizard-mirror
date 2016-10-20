#!/usr/bin/env python
import sys
import os
import glob
import multiprocessing as mp
import inspect
from functools import partial
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import bcn_plot
import data_utils
from utils import load_json

parallel = True


def main():
  print 'Start'
  pic_path = os.path.abspath('./plots') + '/'
  data_path = os.path.abspath('./scan-results')
  data_path2 = os.path.abspath('../ee_tt/scan-results')
  files = glob.glob(data_path + '/*.dat')
  files += glob.glob(data_path2 + '/*.dat')
  data = data_utils.load_and_clean_files(files)
  for idx, item in enumerate(data):
    if 'Analytic' in item[0]:
      data[idx][1][1] *= 1000
  plot_this = partial(bcn_plot.plot, data=data, pic_path=pic_path)
  plot_json = load_json('plot.json')
  if parallel:
    pool = mp.Pool(processes=4)
    pool.map(plot_this, plot_json['plots'])
  else:
    map(plot_this, plot_json['plots'])

main()
