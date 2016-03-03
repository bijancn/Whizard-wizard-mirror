#!/usr/bin/env python
import sys
import os
import glob
import re
import multiprocessing as mp
import numpy as np
import inspect
from functools import partial
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import bcn_plot
from utils import load_json

def ls_decider(lbl, title):
  if 'fixedorder_offshell_NLO_unrestricted' in lbl or 'matched_NLO' in lbl:
    return None
  if 'p0' in lbl and 'expanded' in lbl or 'onshell_NLO' in lbl or 'v_of_sqrts' in lbl:
    return 'dashdot'
  elif 'expanded' in lbl or 'Oneloop' in lbl:
    return 'dashed'
  elif 'p0' in lbl:
    return 'dotted'
  elif 'Analytic' in lbl or 'tree' in lbl or 'nloop' in lbl or 'ratio' in lbl or \
      'switch' in lbl or 'LO' in lbl:
    return 'solid'
  else:
    return None

def m_decider(lbl, title):
  if 'offshell' in lbl:
    return '+'
  elif 'onshell' in lbl:
    return 'x'
  else:
    return 'o'

def _pretty_lbl(l, title):
  l = l.replace('f_switch_off', '$f--s(v(\\sqrt{s}))$')
  l = l.replace('v_of_sqrts', '$v(\\sqrt{s})$')
  if 'offshell' in l and 'LO' in l:
    if not 'unrestricted' in l and not 'signal' in l and not 'full' in l:
      l = l + '_signal'
  l = l.replace('unrestricted', 'full')
  l = re.sub('fixedorder_(.*)', '$\\sigma--\\mathrm{QCD}^\\mathrm{\\1}$', l)
  l = l.replace('Kfactordiff', '$\\sigma--\\mathrm{NLO}-\\sigma--\\mathrm{LO}$')

  sdict = {'soft_hard' : 'f--salpha--S+(1-f--s)alpha--H',
           'hard' : 'alpha--H', '' : 'alpha--H', 'soft' : 'alpha--S'}
  for scale in ['soft_hard', 'hard', 'soft', '']:
    l = re.sub('expanded_' + scale + '_(.*)',
        r'$\sigma--\mathrm{NRQCD}^\mathrm{expanded,\1}[alpha--H,' + sdict[scale] + ']$', l)
  l = l.replace('_mpole172', '')
  l = l.replace('w_nlo', '\\Gamma--\\mathrm{NLO}')
  l = re.sub('_sh_(\d\.\d*)', '', l)
  l = re.sub('_sf_(\d\.\d*)', '', l)
  l = re.sub('resum_nloop_1_full', '$\\sigma--\\mathrm{NRQCD}^\\mathrm{NLL,full}$', l)
  l = re.sub('resum_nloop_1', '$\\sigma--\\mathrm{NRQCD}^\\mathrm{NLL}$', l)
  l = re.sub('resum_nloop_0_full', '$\\sigma--\\mathrm{NRQCD}^\\mathrm{LL,full}$', l)
  l = re.sub('resum_nloop_0', '$\\sigma--\\mathrm{NRQCD}^\\mathrm{LL}$', l)
  l = re.sub('resum_switchoff_nloop_1',
      '$\\sigma--\\mathrm{NRQCD}^\\mathrm{NLL}[f--salpha--s]$', l)
  l = re.sub('resum_switchoff_nloop_0',
      '$\\sigma--\\mathrm{NRQCD}^\\mathrm{LL}[f--salpha--s]$', l)
  # l = l.replace('resum_nloop_0', '$\\sigma--\\mathrm{NRQCD}^\\mathrm{LL}$')
  l = l.replace('matched_NLO', '$\\sigma--\\mathrm{matched}$')

  l = l.replace('nloop_0', 'LL')
  l = l.replace('nloop_1', 'NLL')
  l = re.sub('_plus_', '$+$', l)
  l = re.sub('dm_*(\d+)', '$\\Delta M = \\1 \\;\\mathrm{GeV}$', l)
  l = l.replace('NonrelXsec', '')
  l = re.sub('wtop_(\d\.\d*)', '$w--\\mathrm{top} = \\1 \\;\\mathrm{GeV}$', l)
  l = re.sub('ratio_',
      r'$\\frac{\\sigma--\\mathrm{analytic}}{\\sigma--\\textsc{Whizard}}$, ', l)
  l = l.replace('_', ', ')
  l = re.sub('mpole172', r'$m_{\mathrm{pole}}=m_{1S}$', l)
  l = re.sub('p0', '$p_0$-dependent', l)
  l = re.sub('ONSHELL', 'onshell', l)
  return l

def pretty_label(l, title):
  func = lambda x: _pretty_lbl(x.group(1), title) + '$-$' + _pretty_lbl(x.group(2), title)
  func_div = lambda x: _pretty_lbl(x.group(1), title) + '$/$' + _pretty_lbl(x.group(2), title)
  l = re.sub('(.*)_minus_(.*)', func, l)
  l = re.sub('(.*)_divby_(.*)', func_div, l)
  l = _pretty_lbl(l, title)
  l = l.replace('--', '_')
  l = l.replace('alpha', r'\alpha')
  return l

def plot_extra(ax, title):
  ax.axvline(x=2*172.0, color='lightgray', linestyle='dashed')
  if 'ratio' in title or 'Kfactor' in title:
    ax.axhline(y=1.0, color='lightgray', linestyle='dashed')
  if 'difference' in title or 'matching-stepbystep' in title or \
      'matching-andre' in title:
    ax.axhline(y=0.0, color='lightgray', linestyle='dashed')
  if 'switch-off' in title:
    ax.text(355.0, 0.85, '$v_1=0.1$')
    ax.text(355.0, 0.80, '$v_2=0.3$')
  return ax

def label_decider(title):
  if 'switch-off' in title or 'ratio' in title:
    ylabel = ''
  else:
    ylabel = '$\\sigma$ [fb]'
  return '$\\sqrt{s}$ [GeV]', ylabel

def main ():
  pic_path = os.path.abspath('./plots') + '/'
  data_path = os.path.abspath('./scan-results')
  files = glob.glob(data_path + '/*.dat')
  plot_json = load_json('plot.json')
  data = [(filename, np.loadtxt(filename, unpack=True)) for filename in files]
  pool = mp.Pool(processes=3)
  plot_this = partial(bcn_plot.plot, data=data, pic_path=pic_path)
  pool.map(plot_this, plot_json['plots'])

main()
