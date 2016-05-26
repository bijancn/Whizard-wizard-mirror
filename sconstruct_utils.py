import os
import re
from glob import glob


def filter_existing_processes(proc_list, suffix):
  return filter(lambda p: os.path.isfile(p + '-0.' + suffix), proc_list)


def get_yodas_from_proc_list(proc_list):
  return [glob(p + '-*.yoda') for p in proc_list]


def get_yodas_from_hepmc(hepmcs):
  yodas = []
  replace_hepmc = lambda s : re.sub('.hepmc', '.yoda', str(s))
  for hepmc in hepmcs:
    yodas.append(map(replace_hepmc, hepmc))
  return yodas


def get_final_yoda_names(base_names):
  remove_proc_ids = lambda s : re.sub('-[0-9]+.yoda', '.yoda', str(s[0]))
  return map(remove_proc_ids, base_names)
