import argparse
import numpy as np
from math import sqrt
import os.path

parser = argparse.ArgumentParser(description="Input yoda file name")
parser.add_argument('--yoda', dest='yoda_name', type=str)
parser.add_argument('--search-negative-histograms',
   dest='negative_yodas', type=bool, default=False)
parser.add_argument('--tolerance', dest='tolerance', type=int, default=10)
parser.add_argument('--verbose', dest='verbose', type=bool, default=False)
args = parser.parse_args()

require_bad_rel = 0.25
n_yodas_tot = 80
n_yodas_max = 200


def analyze_all_yodas(base_name, yoda_min, yoda_max):
  area = []
  n_yodas = 0
  if yoda_min < 0 or yoda_max < 0:
    yoda_name = base_name + '.yoda'
    area.append(analyze_yoda(yoda_name))
    n_yodas = 1
  else:
    for yoda_nr in range(yoda_min, yoda_max):
      yoda_name = base_name + '-' + str(yoda_nr) + '.yoda'
      area.append(analyze_yoda(yoda_name))
      n_yodas += 1
  print 'Mean values of all yodas: ', sum(area) / n_yodas


def analyze_yoda(filename):
  searchfile = open(filename, "r")
  area = []
  n_histos = 0

  for line in searchfile:
    if "Area" in line:
       elements = line.split()
       area.append(float(elements[2]))
       n_histos += 1

  return sum(area) / n_histos
  searchfile.close()


def check_yoda_for_negative_histogram(filename):
  searchfile = open(filename, "r")
  negative_histos = []
  histo_nr = 1
  for line in searchfile:
    if "Area" in line:
      elements = line.split()
      if float(elements[2]) < 0.0:
        negative_histos.append(histo_nr)
      histo_nr += 1
  return negative_histos


def search_for_negative_yodas(base_name, yoda_min, yoda_max):
  for yoda_nr in range(yoda_min, yoda_max):
    yoda_name = base_name + '-' + str(yoda_nr) + '.yoda'
    negative_histos = check_yoda_for_negative_histogram(yoda_name)
    if len(negative_histos) > 0:
      print 'Found negative histograms in yoda nr. ', yoda_nr
      print negative_histos
    else:
      print 'Found no negative histograms in yoda nr. ', yoda_nr


class yoda_histo(object):
  def __init__(self, n_bins):
    self.n_bins = n_bins
    self.mean = np.zeros(n_bins)
    self.sum_of_weights = np.zeros(n_bins)
    self.variance = np.zeros(n_bins)
    self.deviant = []

  def __str__(self):
    line = "n_bins: {0}\n mean: {1}\n variance: {2}\n deviating yodas{3}: "
    return line.format(self.n_bins, self.mean, self.variance, self.deviant)


def is_histogram_beginning(line):
  return "BEGIN YODA_HISTO1D" in line


def is_histogram_end(line):
  return "END YODA_HISTO1D" in line


def is_data_beginning(line):
  return "# xlow" in line


def extract_name(line):
  tmp1 = line.split()
  tmp2 = tmp1[2].split("/")
  return tmp2[2]


def compute_elemental_mean(mean, weight, n):
  return mean + (weight - mean) / n


def compute_elemental_variance(variance, mean_old, mean_new, n):
  if (n > 1):
    return variance + n * pow(mean_new - mean_old, 2)
  else:
    return variance


def compute_mean_and_variance(base_name, yoda_histos, n_yoda):
  filename = base_name + '.yoda'
  i_bin = 0
  read_data = False
  try:
    searchfile = open(filename, 'r')
  except:
    print 'WARNING: File ' + filename + ' not found'
    return
  current_name = ''
  for line in searchfile:
    if is_histogram_beginning(line):
      current_name = extract_name(line)
    if current_name in yoda_histos:
      if read_data and i_bin < yoda_histos[current_name].n_bins:
        x = line.split()
        n_entries = int(x[6])
        if n_entries > 0:
          # Pep8 does not like a line break after the = sign.
          # But it does not like long lines either.
          # So, we end up with this stupid looking constructions.
          old_mean = yoda_histos[current_name].mean[i_bin]
          new_mean = compute_elemental_mean(old_mean, float(x[2]), n_yoda)
          yoda_histo[current_name].mean[i_bin] = new_mean
          old_variance = yoda_histos[current_name].variance[i_bin]
          foo = compute_elemental_variance(
              old_variance, old_mean, new_mean, n_yoda)
          yoda_histos[current_name].variance[i_bin] = foo
        i_bin += 1
      else:
        read_data = False
        i_bin = 0
    if not read_data:
      read_data = is_data_beginning(line)
  searchfile.close()


def fill_deviators(base_name, yoda_histos, i_yoda, n_yodas, tolerance):
  filename = base_name + '.yoda'
  i_bin = 0
  read_data = False
  try:
    searchfile = open(filename, 'r')
  except:
    print 'WARNING: File ' + filename + ' not found'
    return
  current_name = ''
  for line in searchfile:
    if is_histogram_beginning(line):
      current_name = extract_name(line)
    if current_name in yoda_histos:
      if read_data and i_bin < yoda_histos[current_name].n_bins:
        x = line.split()
        current_mean = yoda_histos[current_name].mean[i_bin]
        current_sigma = sqrt(yoda_histos[current_name].variance[i_bin] / n_yodas)
        if(abs(current_mean) > 0.0 and current_sigma > 0.0):
          pull = abs(current_mean - float(x[2])) / current_sigma
          if pull > tolerance and i_yoda not in yoda_histos[current_name].deviant:
            yoda_histos[current_name].deviant.append(i_yoda)
        i_bin += 1
      else:
        read_data = False
        i_bin = 0
    if not read_data:
       read_data = is_data_beginning(line)
  searchfile.close()


def loop_over_histos_and_find_deviators(base_name, i_yodas, yoda_histos, tolerance):
  for i_yoda in i_yodas:
    yoda_name = base_name + '-' + str(i_yoda)
    fill_deviators(yoda_name, yoda_histos, i_yoda, len(i_yodas), tolerance)


def find_associated_yodas(base_name):
  i_yodas = []
  for i_yoda in range(n_yodas_max):
    filename = base_name + '-' + str(i_yoda) + '.yoda'
    if os.path.isfile(filename):
       i_yodas.append(i_yoda)
  return i_yodas


def create_histos(base_name, i_yodas):
  reference_yoda = base_name + '-' + str(i_yodas[0]) + '.yoda'
  yoda_histos = {}
  searchfile = open(reference_yoda, 'r')
  n_bins = 0
  count_bins = False
  for line in searchfile:
    if is_histogram_beginning(line):
      name = extract_name(line)
    if count_bins and not is_histogram_end(line):
      n_bins += 1
    elif is_histogram_end(line):
      dict_tmp = {name: yoda_histo(n_bins)}
      yoda_histos.update(dict_tmp)
      n_bins = 0
      count_bins = False
    if not count_bins:
      count_bins = is_data_beginning(line)
  searchfile.close()
  return yoda_histos


def loop_over_all_yodas_and_compute_mean(base_name, i_yodas, yoda_histos):
  n_yodas = 1
  for i_yoda in i_yodas:
    yoda_name = base_name + '-' + str(i_yoda)
    compute_mean_and_variance(yoda_name, yoda_histos, n_yodas)
    n_yodas += 1
  return yoda_histos


def print_all_histos(yoda_histos):
  for name, yh in yoda_histos.items():
    print name
    print yh
    print "**********************"


print 'Initializing histogram objects'
i_yodas = find_associated_yodas(args.yoda_name)
yoda_histos = create_histos(args.yoda_name, i_yodas)
yoda_histos = loop_over_all_yodas_and_compute_mean(args.yoda_name, i_yodas, yoda_histos)
tolerance = args.tolerance
loop_over_histos_and_find_deviators(args.yoda_name, i_yodas, yoda_histos, args.tolerance)
if args.verbose:
  print_all_histos(yoda_histos)
count_deviators = np.zeros(n_yodas_max)
for name, yh in yoda_histos.items():
  for deviator in yh.deviant:
    count_deviators[deviator] += 1

if args.verbose:
  print 'How often does a yoda deviate? ', count_deviators
print 'Require at least ', int(require_bad_rel * len(i_yodas)), ' deviations.'
i_yoda = 0
remove_yodas = []
for counter in count_deviators:
  if counter >= int(require_bad_rel * len(i_yodas)):
    remove_yodas.append(i_yoda)
  i_yoda += 1

print 'Would remove: ', remove_yodas
