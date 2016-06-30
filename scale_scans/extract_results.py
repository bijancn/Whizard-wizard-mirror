#!/usr/bin/env python
import sys
import os
import glob
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
  if filter is not None:
    if filter is not '' and not scaled:
      return []
  nlo = proc_dict['nlo_type'] == 'nlo'
  if not scaled and not nlo:
    full_names = [base_name]
  else:
    if scaled:
      scaled_names = []
      for suffix in get_scale_suffixes():
        if filter is None:
          scaled_names += [base_name]
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


#def get_nlo_suffixes(proc_dict):
#  requires_mismatch = proc_dict.get('fks_method') == 'resonances'
#  requires_dglap_remnant = proc_dict.get('beam_type') == 'hadrons'
#  nlo_suffixes = ['Born', 'Real', 'Virtual']
#  if requires_mismatch:
#    nlo_suffixes.append('Mismatch')
#  if requires_dglap_remnant:
#    nlo_suffixes.append('Dglap')
#  return nlo_suffixes


def is_complete_nlo_set(proc_dict, scale_suffix, result_path):
  complete = 'nlo' in proc_dict['process']
  if not complete:
    return False 
  all_proc = get_full_proc_names (proc_dict['process'], proc_dict, filter=scale_suffix)
  print 'all_proc: ', all_proc
  if len(all_proc) > 0:
    for p in all_proc:
      print 'search for ', result_path + '/' + p + '.dat'
      complete = complete and os.path.isfile(result_path + '/' + p + '.dat') 
    return complete
  else:
    return False


def get_RES (c):
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
      dirs += get_full_proc_names (p['process'], p)
       
  runfolders = ['whizard/' + p for p in dirs]
  result_cmd = [get_RES(runfolder) for runfolder in runfolders]
  result_file = [os.path.join(result_path, p + '.dat') for p in dirs]
  print 'result_cmd: ', result_cmd
  print 'result_file: ', result_file
  for cmd, file in zip(result_cmd, result_file):
    print 'cmd: ', cmd + ' > ' + file
    ret = subprocess.call(cmd + ' > ' + file, shell=True)
    if (ret == 0):
      print '\nSaved to ' + file
    else:
      print '\nSaving to '+ file + ' returned ' + str(ret)
      sys.exit(1)
