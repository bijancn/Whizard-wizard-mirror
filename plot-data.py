#!/usr/bin/env python
import os
import glob
import multiprocessing as mp
import argparse
from functools import partial
import bcn_plot
import data_utils
from utils import load_json

# Parse command line options
parser = argparse.ArgumentParser(description='Plot data',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# options how to behave
parser.add_argument("-j", '--jobs', default=4, type=int,
    help='Set number of jobs for plotting. Use -j1 to disable multiprocessing.')
parser.add_argument("-p", '--plot', type=str,
    help='Select a PLOT according to its output_file.')
args = parser.parse_args()


def find_all_data_paths(cwd, plot_json):
  data_paths = []
  for plot in plot_json['plots']:
    for line in plot.get('lines', []) + plot.get('bands', []):
      data_paths.append(line.get('folder', cwd))
      for bl in line.get('base_line', []):
        data_paths.append(bl.get('folder', cwd))
  data_paths = map(os.path.abspath, data_paths)
  data_paths = [os.path.join(dp, 'scan-results') for dp in data_paths]
  data_paths = list(set(data_paths))
  return data_paths


def main():
  cwd = os.getcwd()
  plot_json = load_json(os.path.join(cwd, 'plot.json'))
  data_paths = find_all_data_paths(cwd, plot_json)
  files = [str(f) for dp in data_paths for f in glob.glob(dp + '/*.dat')]
  pic_path = os.path.abspath(os.path.join(cwd, 'plots')) + '/'
  data = data_utils.load_and_clean_files(files, plot_json)
  for idx, item in enumerate(data):
    if 'Analytic' in item[0]:
      data[idx][1][1] *= 1000
  plot_this = partial(bcn_plot.plot, data=data, pic_path=pic_path)
  plots = plot_json['plots']
  if args.plot is not None:
    plots = [p for p in plots if args.plot in p['output_file']]
  if args.jobs > 1:
    pool = mp.Pool(processes=args.jobs)
    pool.map(plot_this, plots)
  else:
    map(plot_this, plots)

main()
