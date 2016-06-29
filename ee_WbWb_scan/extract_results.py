#!/usr/bin/env python
import sys
import os
import subprocess
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from utils import cd, load_json, mkdirs, fatal
import numpy as np
from math import sqrt
from data_utils import sort_data


def get_scale_suffixes(include_empty=False):
  if include_empty:
    return ['', 'central', 'low', 'high']
  else:
    return ['central', 'low', 'high']


def create_nlo_component_names(sindarin, proc_dict):
  return [sindarin + '_' + s for s in get_component_suffixes(proc_dict)]


def get_component_suffixes(proc_dict):
  suffixes = ['Born', 'Real', 'Virtual']
  if proc_dict.get('fks_method', 'default') == 'resonances':
    suffixes += ['Mismatch']
  if proc_dict.get('beam_type', 'leptons') == 'hadrons':
    suffixes += ['Dglap']
  return suffixes


def get_full_proc_names(base_name, proc_dict, filter=None):
  scaled = proc_dict.get('scale_variation', False)
  nlo = proc_dict['nlo_type'] == 'nlo'
  if not scaled and not nlo:
    full_names = [base_name]
  else:
    if scaled:
      scaled_names = []
      for suffix in get_scale_suffixes():
        if filter is None:
          scaled_names += [base_name + '_' + suffix]
        else:
          if filter == suffix:
            scaled_names += [base_name + '_' + suffix]
    else:
      scaled_names = [base_name]
    if nlo:
      full_names = []
      for scaled_name in scaled_names:
          full_names += create_nlo_component_names(scaled_name, proc_dict)
    else:
      full_names = scaled_names
  return full_names


def is_complete_nlo_set(proc_dict, scale_suffix, result_path):
  complete = 'nlo' in proc_dict['process']
  if not complete:
    return False
  all_proc = get_full_proc_names(proc_dict['process'], proc_dict, filter=scale_suffix)
  if len(all_proc) > 0:
    for p in all_proc:
      print 'search for ', result_path + '/' + p + '.dat'
      complete = complete and os.path.isfile(result_path + '/' + p + '.dat')
    return complete
  else:
    return False


def get_RES(c):
  return "grep RES " + c + "-*/whizard.log | sed 's/^.*RES //'"

try:
  process_folder = sys.argv[1]
except:
  fatal('You have to give me the process directory as argument')
with cd(process_folder):
  result_path = 'scan-results'
  mkdirs(result_path)
  run_json = load_json('run.json')
  processes = [p['process'] for p in run_json['processes'] if p['purpose'] == 'scan']
  uses_scale_variation = [p.get('scale_variation', False) for p in run_json['processes']]
  is_separate_nlo = [p['nlo_type'] == 'nlo' for p in run_json['processes']]
  dirs = []
  for p in run_json['processes']:
    if p['purpose'] == 'scan':
      dirs += get_full_proc_names(p['process'], p)
  runfolders = ['whizard/' + p for p in dirs]
  result_cmd = [get_RES(runfolder) for runfolder in runfolders]
  result_file = [os.path.join(result_path, p + '.dat') for p in dirs]
  for cmd, file in zip(result_cmd, result_file):
    print 'cmd: ', cmd + ' > ' + file
    ret = subprocess.call(cmd + ' > ' + file, shell=True)
    if (ret == 0):
      print '\nSaved to ' + file
    else:
      print '\nSaving to ' + file + ' returned ' + str(ret)
      sys.exit(1)
  for scale in get_scale_suffixes(include_empty=True):
    for p in run_json['processes']:
      if is_complete_nlo_set(p, scale, result_path):
        print 'Found a complete NLO set, scale = ', scale
        first = True
        for nlo_suffix in get_component_suffixes(p):
          print 'nlo_suffix: ', nlo_suffix
          filename = result_path + '/' + p['process']
          if scale is not '':
            filename += '_' + scale
          filename += '_' + nlo_suffix + '.dat'
          with open(filename, 'r') as file:
            if first:
              n_lines = sum(1 for line in file)
              sqrts = np.zeros(n_lines)
              integral = np.zeros(n_lines)
              error = np.zeros(n_lines)
              file.seek(0, 0)  # Rewind file
            i_line = 0
            for line in file:
              if first:
                sqrts[i_line] = float(line.split()[0])
              integral[i_line] += float(line.split()[1])
              error[i_line] += pow(float(line.split()[2]), 2)
              i_line += 1
            first = False
        print 'Evaluated scale: ', scale
        data = [('foo', np.array([sqrts, integral, error]))]
        data = sort_data(data)
        sqrts = data[0][1][0]
        integral = data[0][1][1]
        error = data[0][1][2]
        new_filename = result_path + '/' + p['process']
        if scale is not '':
          new_filename += '_' + scale
        new_filename += '.dat'
        with open(new_filename, 'w') as nfile:
          for i_line in range(len(sqrts)):
            nfile.write(str(sqrts[i_line]) + ' ')
            nfile.write(str(integral[i_line]) + ' ')
            nfile.write(str(sqrt(error[i_line])) + '\n')
      elif '_lo' in p['process']:
        filename = result_path + '/' + p['process'] + '.dat'
        with open(filename, 'r') as file:
          n_lines = sum(1 for line in file)
          sqrts = np.zeros(n_lines)
          integral = np.zeros(n_lines)
          error = np.zeros(n_lines)
          file.seek(0, 0)
          i_line = 0
          for line in file:
            sqrts[i_line] = float(line.split()[0])
            integral[i_line] = float(line.split()[1])
            error[i_line] = float(line.split()[2])
            i_line += 1
          data = [('foo', np.array([sqrts, integral, error]))]
          data = sort_data(data)
          sqrts = data[0][1][0]
          integral = data[0][1][1]
          error = data[0][1][2]
          with open(filename, 'w') as file:
            for i_line in range(len(sqrts)):
              file.write(str(sqrts[i_line]) + ' ')
              file.write(str(integral[i_line]) + ' ')
              file.write(str(error[i_line]) + '\n')
