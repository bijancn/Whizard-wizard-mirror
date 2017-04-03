import argparse

parser = argparse.ArgumentParser(description="Path to .dat-files")
parser.add_argument('--path', dest='path', type=str)
parser.add_argument('--leading-order', dest='is_lo', type=bool)
parser.add_argument('--observable', dest='observable', type=str)
args = parser.parse_args()


def extract_numbers(filename, observable, nlo, scale=''):
  new_histo = False
  read = False
  searchfile = open(filename, "r")
  cos_theta = []
  weights = []
  obs = '/' + observable
  i_weight = get_weight_indices(filename, scale)
  check_start = start_string(filename)
  for line in searchfile:
    if "BEGIN YODA" in line and obs in line:
      new_histo = True
    if "END YODA" in line:
      new_histo = False
      read = False
    if read:
      x = line.split()
      cos_theta.append(float(x[0]))
      weights.append(sum(float(x[i]) for i in i_weight))
    if new_histo and check_start in line:
      read = True
  return cos_theta, weights


def get_weight_indices(filename, scale):
  if 'envelope' in filename:
    if scale == 'central':
      i_weight = [3]
    elif scale == 'low':
      i_weight = [3, 4]
    elif scale == 'high':
      i_weight = [3, 5]
  else:
    i_weight = [2]
  return i_weight


def start_string(filename):
  if 'envelope' in filename:
    check_start = "xval"
  else:
    check_start = "xlow"
  return check_start


def compute_afb_from_list(cos_theta, weight):
  sumwp = 0.0
  sumwm = 0.0
  for x, w in zip(cos_theta, weight):
    if x <= 0.0:
       sumwm += w
    else:
       sumwp += w
  return (sumwp - sumwm) / (sumwp + sumwm)

# filename = os.path.join(args.path, args.observable + '.dat')
filename = args.path
nlo = not args.is_lo
if nlo and 'envelope' in filename:
  scales = ['central', 'low', 'high']
elif nlo and 'proc_nlo' in filename:
  foo = filename.split('/')
  proc = foo[len(foo) - 1]
  scales = [proc.split('_')[2].split('.')[0]]
else:
  scales = []

afb = []

if nlo:
  for scale in scales:
    cth, w = extract_numbers(filename, args.observable, True, scale)
    this_afb = compute_afb_from_list(cth, w)
    afb.append(this_afb)
  if (len(scales) > 1):
    corr_minus = (afb[1] - afb[0]) / afb[0] * 100
    corr_plus = (afb[2] - afb[0]) / afb[0] * 100
    print 'afb: ', afb[0], ' + ', corr_plus, '%   ', corr_minus, '%'
  else:
    print 'scale: ', scale, 'afb: ', afb[0]
else:
  cth, w = extract_numbers(filename, args.observable, False)
  print 'cth: ', cth
  print 'w: ', w
  this_afb = compute_afb_from_list(cth, w)
  afb.append(this_afb)
  print 'LO: ', this_afb
