import argparse
import numpy as np
from math import sqrt
import os.path

parser = argparse.ArgumentParser(description="Input yoda file name")
parser.add_argument('--data', dest='data', type=str)
args = parser.parse_args()

def compute_sumw (filename):
  searchfile = open(filename, "r")
  sumwp = 0
  sumwm = 0
  read = False
  new_histo = False
  labels = []
  sumwp_list = []
  sumwm_list = []
  for line in searchfile:
    if "BEGIN HISTO1D" in line: new_histo = True
    if "END HISTO1D" in line:
       new_histo = False
       read = False
       sumwp_list.append (sumwp)
       sumwm_list.append (sumwm)
       sumwp = 0
       sumwm = 0
    if new_histo and "Title" in line:
       labels.append (line.split('=')[1])
    if read:
      x = line.split()
      if float (x[0]) <= 0.0:
        sumwm += float (x[2])
      else:
        sumwp += float (x[2])
    if "xlow" in line: read = True
  return labels, sumwm_list, sumwp_list

print 'Computing top forward-backward asymmetry'
labels, sumwm, sumwp = compute_sumw (args.data)
for i_histo in range(len(labels)):
  print 'Process: ', labels[i_histo]
  print 'afb: ', (sumwp[i_histo] - sumwm[i_histo]) / (sumwp[i_histo] + sumwm[i_histo])  

