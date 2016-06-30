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
from utils import load_json
import data_utils


def ls_decider(lbl, title):
  return "solid"


def pretty_label(l, title):
  l = os.path.basename(l)
  l = l.replace('proc_lo', '$t \\bar t$')
  l = l.replace('proc_nlo', '$t \\bar t$')
  l = l.replace('.dat', '')
  return l


def plot_x_axis(ax, title):
  ax.axhline(0)
  return ax


def main():
  pic_path = os.path.abspath('./plots') + '/'
  data_path = os.path.abspath('./scan-results')
  data_path2 = os.path.abspath('../ee_tth_scan/scan-results')
  data_path3 = os.path.abspath('../scale_scans/scan-results')
  files = glob.glob(data_path + '/*.dat')
  files += glob.glob(data_path2 + '/*.dat')
  files += glob.glob(data_path3 + '/*.dat')
  plot_json = load_json('plot.json')
  data = data_utils.load_and_clean_files(files, plot_json)
  pool = mp.Pool(processes=3)
  plot_this = partial(bcn_plot.plot, plot_extra=plot_x_axis, data=data,
      pic_path=pic_path, linestyle_decider=ls_decider, pretty_label=pretty_label)
  pool.map(plot_this, plot_json['plots'])

main()
