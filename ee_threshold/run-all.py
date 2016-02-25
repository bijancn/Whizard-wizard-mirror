from time import sleep
from mpi4py_map import mpi_map, comm
from subprocess import call
from subproc import replace_file, whizard_run
from utils import cd, mkdirs
from numpy import arange
import shutil
import os

res_path = '/data/bcho/whizard_ttbar_threshold_project/Data/validation/'
dryrun = True
dryrun = False

def get_RES (c):
  return "grep RES " + c + "-*/whizard.log | sed 's/^.*RES //'"

def setup(curve):
  print 'Setting up ', curve
  call('./create-sindarin.sh ' + curve + ' &> /dev/null', shell=True)
  return 'Done with setup of ' + curve

def run_curve(curve):
  run_folder = curve[0] + '/' + curve[0]
  sindarin = run_folder + '/run.sin'
  runfolder = run_folder + '-' + str(curve[2])
  mkdirs(runfolder)
  shutil.copyfile(sindarin, os.path.join(runfolder, 'run.sin'))
  with cd(runfolder):
    replace_file('run.sin', curve[1], curve[2])
    call('rm -f *grid', shell=True)
    if (not dryrun and not os.path.isfile('done')):
      print 'Running ' + runfolder
      ret = whizard_run('whizard -r', 'run.sin')
      # ret = whizard_run('whizard', 'run.sin')
      if ret != 0:
        print runfolder + ' Whizard return code ' + str(ret)
        return runfolder + ' Whizard return code ' + str(ret)
        # raise Exception(runfolder, 'Whizards return code', ret)
      else:
        with open('done', 'a'):
          os.utime('done', None)
          print 'done with ' + runfolder
          return 'done with ' + runfolder
    else:
      # print 'Skipping ' + runfolder
      return 'skipping ' + runfolder

def final(curve):
  run_folder = curve + '/' + curve
  results = get_RES(run_folder)
  res_file = res_path + curve + '.dat'
  ret = call(results + ' > ' + res_file, shell=True)
  if (ret == 0):
    strg = '\nSaved to ' + res_file
  else:
    strg = '\nSaving to '+ res_file + ' returned ' + ret
  print strg
  return strg

def do_all((fct_tag, obj)):
  if fct_tag == 0:
    return setup(obj)
  elif fct_tag == 1:
    return run_curve(obj)
  elif fct_tag == 2:
    return final(obj)
  else:
    raise

curves = []
modes = ['resum_switchoff', 'matched_minus_NLO', 'resum', 'expanded_soft',
         'expanded_hard', 'expanded_switchoff', 'expanded_soft_hard']
for nloop in range(2):
  for mode in modes:
    curves += [mode + '_nloop_' + str(nloop) + '_sh_1._sf_1._mpole172']
curves += ['fixedorder_offshell_LO']
curves += [c + '_unrestricted' for c in curves]
curves += ['fixedorder_offshell_NLO_unrestricted', 'fixedorder_offshell_NLO',
           'fixedorder_onshell_NLO', 'fixedorder_onshell_LO',
           'fixedorder_offshell_LO_unrestricted_w_nlo']
for v2 in ['2', '3', '4', '5', '6', '7', '8', '9']:
  curves += ['matched_minus_NLO_nloop_1_sh_1._sf_1._mpole172_unrestricted_v2_0.' + v2]
curves += ['tree_pole_approx_LO_mpole172']
curves += ['resum_nloop_1_sh_1._sf_1._mpole172_pole_approx_LO']
curves += ['resum_nloop_1_sh_1._sf_1._mpole172_width_LO']
curves += ['resum_nloop_1_sh_1._sf_1._mpole172_width_LO_unrestricted']

curves_ulo = [(curve, 'sqrts', 300, 340, 1.0) for curve in curves]
curves_lo = [(curve, 'sqrts', 340, 350, 0.25) for curve in curves]
curves_hi = [(curve, 'sqrts', 350, 400, 1.0) for curve in curves]
curves_uhi = [(curve, 'sqrts', 400, 1000, 10.0) for curve in curves if 'fixedorder' in curve]
all_curves = curves_hi + curves_lo + curves_uhi + curves_ulo
runs = [(c[0], c[1], cc) for c in all_curves for cc in list(arange(c[2], c[3], c[4]))]
if comm.Get_rank() == 0:
  print 'Total number of runs:', len(runs)
  print 'Total number of cores:', comm.Get_size()
  print 'Total number of runs/node:', len(runs) / comm.Get_size()
  print 'Setting up folders'
  map(do_all, [(0, c) for c in curves])
comm.Barrier()
mpi_map(do_all, [(1, c) for c in runs])
if comm.Get_rank() == 0:
  print 'Im all done and I export results now'
  map(do_all, [(2, c) for c in curves])
