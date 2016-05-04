import argparse
from math import sqrt

parser = argparse.ArgumentParser(description="Input yoda file name")
parser.add_argument('--data', dest='data', type=str)
args = parser.parse_args()

print 'Computing top forward-backward asymmetry in ', args.data

searchfile = open(args.data, "r")
sumwp = 0
sumwm = 0
varp = 0
varm = 0
read = False
new_histo = False
for line in searchfile:
  if "BEGIN HISTO1D" in line: new_histo = True
  if "END HISTO1D" in line:
     n1 = sumwp - sumwm
     n2 = sumwp + sumwm 
     sigma = sqrt (varp + varm)
     sigma_afb = sqrt (pow (sigma / n2, 2) * (1 + pow (n1 / n2, 2)))
     print 'afb: ', n1 / n2, ' +- ', sigma_afb
     new_histo = False
     read = False
     sumwp = 0
     sumwm = 0
     varp = 0
     varm = 0
  if new_histo and "Title" in line:
     print 'Histogram: ', line.split('=')[1]
     #labels.append (line.split('=')[1])
  if read:
    x = line.split()
    if float (x[0]) <= 0.0:
      sumwm += float(x[2])
      varm += float(x[3]) * float(x[3])
    else:
      sumwp += float(x[2])
      varp += float(x[3]) * float(x[3])
  if "xlow" in line: read = True

