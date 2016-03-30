#!/usr/bin/env python
import sys
import os
import subprocess
from utils import cd, load_json, mkdirs, fatal


def get_RES(c):
  return "grep RES " + c + "-*/whizard.log | sed 's/^.*RES //'"


def main():
  try:
    process_folder = sys.argv[1]
  except:
    fatal('You have to give me the process directory as argument')
  with cd(process_folder):
    result_path = 'scan-results'
    mkdirs(result_path)
    run_json = load_json('run.json')
    processes = [p['process'] for p in run_json['processes'] if p['purpose'] == 'scan']
    print 'processes = ', processes
    runfolders = ['whizard/' + p for p in processes]
    print 'runfolders = ', runfolders
    result_cmd = [get_RES(runfolder) for runfolder in runfolders]
    print 'result_cmd = ', result_cmd
    result_file = [os.path.join(result_path, p + '.dat') for p in processes]
    print 'result_file = ', result_file
    for cmd, file in zip(result_cmd, result_file):
      print 'cmd = ', cmd + ' > ' + file
      ret = subprocess.call(cmd + ' > ' + file, shell=True)
      if (ret == 0):
        print '\nSaved to ' + file
      else:
        print '\nSaving to ' + file + ' returned ' + str(ret)
        sys.exit(1)

main()
