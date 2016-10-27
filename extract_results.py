#!/usr/bin/env python
import sys
import os
import subprocess
import whizard_wizard
from utils import cd, mkdirs, fatal


def get_RES(c):
  return "grep RES " + c + "/whizard.log | sed 's/^.*RES //'"


def build_regexs(proc):
  proc_regexs = [proc[1]]
  for nscans, scan in enumerate(proc[2]['scans']):
    if nscans > 0:
      proc_regexs = [pr + '-' for pr in proc_regexs]
    if scan.get('export_type', '') == 'separate':
      old = proc_regexs
      new = []
      for sc in scan['ranges'][0].get('range', None):
        new += [pr + '-' + str(sc) + '-' + scan['scan_object'] for pr in old]
      proc_regexs = new
    else:
      proc_regexs = [pr + '-*-' + scan['scan_object'] for pr in proc_regexs]
  if proc[2].get('integration_copies', 0) > 0:
    proc_regexs = [pr + '-*' for pr in proc_regexs]
  return proc_regexs


def main():
  try:
    process_folder = sys.argv[1]
  except:
    fatal('You have to give me the process directory as argument')
  else:
    with cd(process_folder):
      result_path = 'scan-results'
      mkdirs(result_path)
      run_json = whizard_wizard.retrieve_and_validate_run_json('.')
      process_runs = whizard_wizard.fill_all_runs(run_json)
      # TODO: (bcn 2016-07-15) for now we only support separate export
      # 2D export could be relevant as well
      process_names = []
      for proc in process_runs:
        if proc[2]['purpose'] == 'scan':
          process_names += build_regexs(proc)
      process_names = list(set(process_names))
      runfolders = ['whizard/' + p for p in process_names]
      for rf in runfolders:
        print 'runfolders = ', rf
      result_cmd = [get_RES(runfolder) for runfolder in runfolders]
      result_files = [os.path.join(result_path, p.replace('-*', '') + '.dat')
          for p in process_names]
      print 'result_files = ', result_files
      for cmd, file_name in zip(result_cmd, result_files):
        ret = subprocess.call(cmd + ' > ' + file_name, shell=True)
        if (ret == 0):
          print 'Saved to ' + file_name
        else:
          print 'Saving to ' + file_name + ' returned ' + str(ret)
          sys.exit(1)

main()
