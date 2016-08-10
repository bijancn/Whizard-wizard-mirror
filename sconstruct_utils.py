import os
import re
from glob import glob


def nlo_process(ps):
  return [ps + '_Born', ps + '_Real', ps + '_Virtual']


def filter_existing_processes(proc_list, suffix):
  return filter(lambda p: os.path.isfile(p + '-0.' + suffix), proc_list)


def get_yodas_from_hepmc(hepmcs):
  replace_hepmc = lambda s : re.sub('.hepmc', '.yoda', str(s))
  return map(replace_hepmc, hepmcs)


def get_yodas_from_proc_list(proc_list):
  yodas = []
  for process in proc_list:
    hepmcs = glob(process + '-*.hepmc')
    if len(hepmcs) > 0:
      yodas.append(get_yodas_from_hepmc(hepmcs))
    else:
      yodas.append(glob(process + '-*.yoda'))
  return yodas


def get_final_yoda_names(base_names):
  results = []
  for s in base_names:
    try:
      results.append(re.sub('-[0-9]+.yoda', '.yoda', str(s[0])))
    except IndexError:
      pass
  return results


def find_nlo_yodas(merged_yodas):
  nlo_yodas = {}
  for yoda in merged_yodas:
    for comp in ['Born', 'Real', 'Virtual']:
      if '_' + comp in str(yoda[0]):
        target = str(yoda[0]).replace('_' + comp, '')
        try:
          nlo_yodas[target].append(yoda[0])
        except KeyError:
          nlo_yodas[target] = [yoda[0]]
        break
  return nlo_yodas


# TODO: (bcn 2016-05-26) Add test

def find_scale_variation_yodas(merged_yodas):
  scale_variation_yodas = {
      'proc_lo_low_yodas': [],
      'proc_lo_central_yodas': [],
      'proc_lo_high_yodas': [],
      'proc_nlo_low_yodas': [],
      'proc_nlo_central_yodas': [],
      'proc_nlo_high_yodas': []}
  for yoda in merged_yodas:
    if 'nlo_low' in str(yoda):
      scale_variation_yodas['nlo_low'].append(yoda)
    elif 'nlo_central' in str(yoda):
      scale_variation_yodas['proc_nlo_central'].append(yoda)
    elif 'nlo_high' in str(yoda):
      scale_variation_yodas['proc_nlo_high'].append(yoda)
    elif 'lo_low' in str(yoda):
      scale_variation_yodas['proc_lo_low'].append(yoda)
    elif 'lo_central' in str(yoda):
      scale_variation_yodas['proc_lo_central'].append(yoda)
    elif 'lo_high' in str(yoda):
      scale_variation_yodas['proc_lo_high'].append(yoda)
  return scale_variation_yodas
