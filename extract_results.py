#!/usr/bin/env python
import sys
import os
import subprocess
import whizard_wizard
from utils import cd, load_json, mkdirs, fatal


def get_RES(c):
  return "grep RES " + c + "-*/whizard.log | sed 's/^.*RES //'"


def main():
  try:
    process_folder = sys.argv[1]
  except:
    fatal('You have to give me the process directory as argument')
  else:
    with cd(process_folder):
      result_path = 'scan-results'
      mkdirs(result_path)
      run_json = load_json('run.json')
      process_runs = whizard_wizard.fill_all_runs(run_json)
      process_names = [p[1] for p in process_runs if p[2]['purpose'] == 'scan']
      process_names = list(set(process_names))
      runfolders = ['whizard/' + p for p in process_names]
      print 'runfolders = ', runfolders
      result_cmd = [get_RES(runfolder) for runfolder in runfolders]
      result_files = [os.path.join(result_path, p + '.dat') for p in process_names]
      print 'result_files = ', result_files
      for cmd, file in zip(result_cmd, result_files):
        ret = subprocess.call(cmd + ' > ' + file, shell=True)
        if (ret == 0):
          print 'Saved to ' + file
        else:
          print 'Saving to ' + file + ' returned ' + str(ret)
          sys.exit(1)

main()
