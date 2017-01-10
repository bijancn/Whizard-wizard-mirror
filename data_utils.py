# various data manipulation functions

import numpy as np
import nose.tools as nt
import os
from scipy.signal import savgol_filter
from termcolor import colored
import fit_utils


def show_means(process_string, data):
  strings = []
  for d in data:
    if process_string in d[0]:
      num_data = d[1]
      mean_mean = np.average(num_data[1])
      try:
        mean_error = np.average(num_data[2])
        strings.append(os.path.basename(d[0]).replace('.dat', '') + ' ' +
            str(mean_mean) + ' ' + str(mean_error) + ' ' + str(mean_error /
            mean_mean * 100) + ' % ' + str(len(num_data[1])))
      except IndexError:
        strings.append(os.path.basename(d[0]).replace('.dat', '') + ' ' +
            str(mean_mean) + ' ' + str(len(num_data[1])))
  strings.sort()
  for string in strings:
    print string


def test_show_means():
    test_string = 'foo'
    test_data = [('foofoo', np.array((np.array([1, 2, 3]), np.array([11, 12, 13])))),
                 ('foobar', np.array((np.array([1, 2, 3]), np.array([21, 22, 23]))))]
    show_means(test_string, test_data)


def remove_empty_data(data):
  for index, item in enumerate(data):
    try:
      x = item[1][0]
      y = item[1][1]
      if x.size < 1 or y.size < 1:
        raise IndexError
    except IndexError:
      print 'Removing empty data from data list: ', data[index][0]
      del data[index]
      # As the del changes what data[index] means, we have to call again
      remove_empty_data(data)
  return data


def test_remove_empty_data():
  test_file = 'foo.dat'
  with open(test_file, 'w') as t:
    t.write('')
  data = [(test_file, np.loadtxt(test_file, unpack=True))]
  nt.eq_(len(data), 1)
  data = remove_empty_data(data)
  nt.eq_(len(data), 0)
  with open(test_file, 'w') as t:
    t.write('0.7')
  data = [(test_file, np.loadtxt(test_file, unpack=True))]
  nt.eq_(len(data), 1)
  data = remove_empty_data(data)
  nt.eq_(len(data), 0)
  with open(test_file, 'w') as t:
    t.write('0.7 1.3')
  data = [(test_file, np.loadtxt(test_file, unpack=True))]
  nt.eq_(len(data), 1)
  data = remove_empty_data(data)
  nt.eq_(len(data), 1)
  os.remove(test_file)


def sort_data(data):
  for index, item in enumerate(data):
    try:
      x = item[1][0]
    except IndexError:
      print 'It seems you still have empty data: ', item
    else:
      if x.size > 1:
        rest = item[1][1:]
        order = np.argsort(x)
        rest_lst = [rest[idx][order] for idx in range(rest.shape[0])]
        array = np.vstack(tuple([x[order]] + rest_lst))
        data[index] = (item[0], array)
  return data


def test_sort_data():
  data = [('foo', np.array([[0.1, 0.3, -5.0, 8, 1E0], [1, 2, 3, 4, 5]]))]
  data = sort_data(data)
  expectation = np.array([[-5.0, 0.1, 0.3, 1.0, 8], [3, 1, 2, 5, 4]])
  np.testing.assert_array_almost_equal(data[0][1], expectation)
  data = [('foo', np.array([[0.1, -5.0], [1, 2], [0.1, 0.2]]))]
  data = sort_data(data)
  expectation = np.array([[-5.0, 0.1], [2, 1], [0.2, 0.1]])
  np.testing.assert_array_almost_equal(data[0][1], expectation)


def get_name(line, custom_name=None):
  folder = line.get('folder', '.')
  if custom_name is None:
    custom_name = line.get('name', None)
  path = os.path.abspath(os.path.join(folder, 'scan-results', custom_name))
  return path


def get_associated_plot_data(data, special, suffix=""):
  """This returns a list of lists of data tuples.

  This list of list is important for bands because you have to know which lines
  belong to a set.
  """
  special_data = []
  list_of_data = [s.get('data', []) for s in special]
  for lbl_list in list_of_data:
    this_special_data = []
    for lbl in lbl_list:
      this_special_data += [d for d in data
          if get_name(lbl) + suffix == d[0].replace('.dat', '')]
    special_data += [this_special_data]
  return special_data


def get_associated_plot_data_single(data, special, suffix=""):
  """This returns a list of data tuples.
  """
  special_data = []
  list_of_lbls = special.get('data', [])
  for lbl in list_of_lbls:
    special_data += [d for d in data
        if get_name(lbl) + suffix == d[0].replace('.dat', '')]
  return special_data


def build_nlo_sums(data):
  for index, item in enumerate(data):
    if '_Born' in item[0]:
      try:
        real_index = next((i for i, x in enumerate(data) if
          item[0].replace('_Born', '_Real') == x[0]))
        virtual_index = next((i for i, x in enumerate(data) if
          item[0].replace('_Born', '_Virtual') == x[0]))
        indices = [index, real_index, virtual_index]
        try:
          mismatch_index = next((i for i, x in enumerate(data) if
            item[0].replace('_Born', '_Mismatch') == x[0]))
          indices += [mismatch_index]
        except StopIteration:
          pass
        combined_x, combined_y, combined_yerr = build_sum(data, indices)
        combined_name = item[0].replace('_Born', '')
        array = np.array((combined_x, combined_y, combined_yerr))
        print 'Appending ' + combined_name
        data.append((combined_name, array))
      except StopIteration:
        pass
    if False:
      show_scale_variations(data)
  return data


def show_scale_variations(data):
  xs_low = 0
  xs_central = 0
  xs_high = 0
  for data_item in data:
    #  TODO: (bcn 2016-10-31) should be steerable from plot.json
    sqrts = 500
    if 'nlo_central' in data_item[0]:
      i_sqrts = np.where(data_item[1][0] == sqrts)[0][0]
      xs_central = data_item[1][1][i_sqrts]
    elif 'nlo_high' in data_item[0]:
      i_sqrts = np.where(data_item[1][0] == sqrts)[0][0]
      xs_high = data_item[1][1][i_sqrts]
    elif 'nlo_low' in data_item[0]:
      i_sqrts = np.where(data_item[1][0] == sqrts)[0][0]
      xs_low = data_item[1][1][i_sqrts]
    elif 'lo' in data_item[0]:
      i_sqrts = np.where(data_item[1][0] == sqrts)[0][0]
      xs_lo = data_item[1][1][i_sqrts]
  if (xs_central > 0):
    k = xs_central / xs_lo
    print '***************'
    print 'sqrts: ', sqrts
    print 'LO: ', xs_lo
    print 'central: ', xs_central
    print 'scale_plus: ', (xs_high - xs_central) / xs_central * 100
    print 'scale_low: ', (xs_central - xs_low) / xs_central * 100
    print 'k-central: ', k
    print 'k-plus: ', (xs_high - xs_central) / xs_lo / k * 100
    print 'k-minus: ', (xs_central - xs_low) / xs_lo / k * 100


def build_smooth(data, smooth_dict):
  if smooth_dict is None:
    return data
  smooth_data = get_associated_plot_data(data, smooth_dict)
  for data_of_a_smooth, smooth in zip(smooth_data, smooth_dict):
    for this_data in data_of_a_smooth:
      x_start = smooth.get('start_at', this_data[1][0][0])
      if x_start != this_data[1][0][0]:
        i_start = min(enumerate(this_data[1][0]), key=lambda x: abs(x[1] - x_start))
        x = this_data[1][0][i_start[0]:]
        y = this_data[1][1][i_start[0]:]
      else:
        x = this_data[1][0]
        y = this_data[1][1]
      smooth_x, smooth_y = smooth_data_sg(x, y,
          window_size=smooth.get('window_size', 0),
          poly_order=smooth.get('poly_order', 3))
      if x_start != this_data[1][0][0]:
        non_smooth_x = np.array(this_data[1][0][0 : i_start[0] - 1])
        non_smooth_y = np.array(this_data[1][1][0 : i_start[0] - 1])
        smooth_x = np.concatenate((non_smooth_x, smooth_x))
        smooth_y = np.concatenate((non_smooth_y, smooth_y))
      smooth_name = this_data[0].replace('.dat', '_smooth.dat')
      print 'Appending ' + smooth_name
      data.append((smooth_name, np.array((smooth_x, smooth_y))))
  return data


def build_fits(data, plot_json):
  fit_dict = plot_json.get('fits', None)
  if fit_dict is None:
    return data
  fit_data = get_associated_plot_data(data, fit_dict)
  for data_of_a_fit, fit in zip(fit_data, fit_dict):
    degree = fit['fit_degree']
    verbose = fit.get('print_fit_parameters', False)
    for this_data in data_of_a_fit:
      x = this_data[1][0]
      xmin = fit.get('extrapolation_minus', min(x))
      xmax = fit.get('extrapolation_plus', max(x))
      y = this_data[1][1]
      y_err = this_data[1][2]
      fit_x, fit_y = fit_utils.fit_polynomial(x, y, xmin, xmax, degree,
        y_err=y_err, verbose=verbose)
      fit_name = this_data[0].replace('.dat', '_fit.dat')
      print 'Appending ' + fit_name
      data.append((fit_name, np.array((fit_x, fit_y))))
  return data


def build_binary_function(data, action_dict):
  action_data = get_associated_plot_data_single(data, action_dict)
  infix = action_dict.get('infix', '_sum_')
  try:
    binary_name = action_data[0][0].replace('.dat',
        infix + os.path.basename(action_data[1][0]))
  except IndexError:
      print 'Warning: You have to give two data sets to binary function.' + \
          ' Skipping: ', action_dict
  else:
    print 'Appending ', binary_name
    common_x, combined_y = remove_uncommon(
        [action_data[0][1][0], action_data[1][1][0]],
        [action_data[0][1][1], action_data[1][1][1]])
    user_func = eval(action_dict.get('expression', 'lambda x,y: x + y'))
    new_y = user_func(combined_y[0], combined_y[1])
    data.append((binary_name, np.array((common_x, new_y))))
    return data


def test_build_binary_function():
  cwd = os.getcwd()
  x_array = np.array((1, 2, 3))
  data = [(cwd + '/scan-results/foo.dat',
           np.vstack((x_array, np.array((10, 20, 30))))),
          (os.path.abspath(cwd + '/../other/scan-results/bar.dat'),
           np.vstack((x_array, np.array((30, 20, 10)))))]
  action_dict = {'data': [
      {'name': 'foo', 'folder': './'},
      {'name': 'bar', 'folder': '../other'}]}
  data = build_binary_function(data, action_dict)
  nt.eq_(data[2][0], cwd + '/scan-results/foo_sum_bar.dat')
  np.testing.assert_array_equal(data[2][1][0], x_array)
  np.testing.assert_array_equal(data[2][1][1], np.array((40, 40, 40)))


def remove_uncommon(list_of_x_arrays, list_of_y_arrays):
  x_generators = [(value for value in array) for array in list_of_x_arrays]
  y_generators = [(value for value in array) for array in list_of_y_arrays]
  combiner = Combiner(x_generators, y_generators,
      [len(array) for array in list_of_x_arrays])
  combined_x, combined_y = combiner.get_all()
  return combined_x, combined_y


def test_remove_uncommon():
  x_list = [np.array([1., 2., 3.]), np.array([2., 3.])]
  y_list = [np.array([.1, .2, .4]), np.array([.2, .3])]
  comb_x, comb_y = remove_uncommon(x_list, y_list)
  np.testing.assert_array_equal(comb_x, x_list[1])
  expectation = [np.array([.2, .4]), np.array([.2, .3])]
  for cy, exp in zip(comb_y, expectation):
    np.testing.assert_array_equal(cy, exp)

  x_list = [np.array([1., 3.]), np.array([2., 3.])]
  y_list = [np.array([.1, .4]), np.array([.2, .3])]
  comb_x, comb_y = remove_uncommon(x_list, y_list)
  np.testing.assert_array_equal(comb_x, np.array(3.))
  expectation = [np.array([.4]), np.array([.3])]
  for cy, exp in zip(comb_y, expectation):
    np.testing.assert_array_equal(cy, exp)

  x_list = [np.array([1., 4.]), np.array([1., 5.])]
  y_list = [np.array([.1, .2]), np.array([.3, .4])]
  comb_x, comb_y = remove_uncommon(x_list, y_list)
  np.testing.assert_array_equal(comb_x, np.array(1.))
  expectation = [np.array([.1]), np.array([.3])]
  for cy, exp in zip(comb_y, expectation):
    np.testing.assert_array_equal(cy, exp)


def normalize(base_line, x, y, yerr=None):
  if len(x) != len(y):
    raise Exception("len(x) /= len(y)")
  x_gens = [(xx for xx in x), (xx for xx in base_line[0])]
  y_gens = [(yy for yy in y), (yy for yy in base_line[1])]
  lengths = [len(array) for array in [x, base_line[0]]]
  divide = lambda lst: reduce(lambda x, y: x / y, lst)
  if yerr is not None:
    if len(x) != len(yerr):
      raise Exception("len(x) /= len(yerr)")
    try:
      yerr_gens = [(yyerr for yyerr in yerr), (yyerr for yyerr in base_line[2])]
    except IndexError:
      print 'Warning: Duplicating yerr in normalize. This can give unexpected' + \
          'results when you input arrays with different lengths!'
      yerr_gens = [(yyerr for yyerr in yerr), (yyerr for yyerr in yerr)]
    error_func = lambda self: self.next_yerr_values / self.next_y_values[1]
  else:
    yerr_gens = None
    error_func = None
  combiner = Combiner(x_gens, y_gens, lengths,
      yerr_generators=yerr_gens, error_func=error_func, operation=divide)
  tmp = combiner.get_all()
  try:
    return tmp[0], tmp[1], tmp[2][0]
  except:
    return tmp[0], tmp[1]


def test_normalize():
  # input is smaller than baseline
  test_baseline = (np.array([1., 2.]), np.array([10., 10.]))
  test_x = np.array([1.])
  test_y = np.array([15.])
  combined_x, combined_y = normalize(test_baseline, test_x, test_y)
  np.testing.assert_array_almost_equal(combined_x, test_x)
  np.testing.assert_array_almost_equal(combined_y, np.array([1.5]))

  test_x = np.array([1., 2.])
  test_y = np.array([15., 20.])
  test_yerr = np.array([1.5, 2.0])
  combined_x, combined_y, combined_yerr = normalize(test_baseline, test_x,
      test_y, yerr=test_yerr)
  np.testing.assert_array_almost_equal(combined_x, test_x)
  np.testing.assert_array_almost_equal(combined_y, np.array([1.5, 2.0]))
  np.testing.assert_array_almost_equal(combined_yerr, np.array([.15, .20]))

  test_baseline = (np.array([1.]), np.array([10.]))
  test_x = np.array([1., 2.])
  test_y = np.array([15., 20.])
  test_yerr = np.array([15., 15.])
  combined_x, combined_y, combined_yerr = normalize(test_baseline,
     test_x, test_y, test_yerr)
  np.testing.assert_array_almost_equal(combined_x, np.array([1.]))
  np.testing.assert_array_almost_equal(combined_y, np.array([1.5]))
  np.testing.assert_array_almost_equal(combined_yerr, np.array([1.5]))

  test_baseline = (np.array([1., 2., 3.]), np.array([10., 10., 10.]))
  test_x = np.array([1., 2., 3.])
  test_y = np.array([0., 20., 0.])
  test_yerr = np.array([0., 15., 0.])
  combined_x, combined_y, combined_yerr = normalize(test_baseline,
     test_x, test_y, test_yerr)
  np.testing.assert_array_almost_equal(combined_x, np.array([1., 2., 3.]))
  np.testing.assert_array_almost_equal(combined_y, np.array([0., 2., 0.]))
  np.testing.assert_array_almost_equal(combined_yerr, np.array([0., 1.5, 0.]))


def combine_and_project(data, indices, operation, error_func):
  unpacked_data = [data[i][1] for i in indices]
  x_generators = [(value for value in array[0]) for array in unpacked_data]
  y_generators = [(value for value in array[1]) for array in unpacked_data]
  yerr_generators = [(value for value in array[2]) for array in unpacked_data]
  lengths = [len(array[0]) for array in unpacked_data]
  combiner = Combiner(x_generators, y_generators, lengths,
      yerr_generators=yerr_generators, error_func=error_func, operation=operation)
  tmp = combiner.get_all()
  try:
    return tmp[0], tmp[1], tmp[2][0]
  except:
    return tmp[0], tmp[1]


def build_sum(data, indices):
  error_func = lambda self: np.sqrt(sum([yerr**2 for yerr in self.next_yerr_values]))
  return combine_and_project(data, indices, sum, error_func)


def build_ratio(data, indices):
  error_func = lambda self: np.sqrt(sum([yerr**2 for yerr in self.next_yerr_values]))
  raise Exception("This is not the correct error function. Please fix first.")
  return combine_and_project(data, indices, lambda x, y: x / y, error_func)


def get_variance(sigma):
  if np.isclose(sum(sigma), 0.0):
    print 'Warning: sum(sigma) = 0. Weighted average doesnt make sense'
    return 0.0
  sum_var_inv = sum([1.0 / (s * s) for s in sigma
      if not np.isclose(s, 0.0, atol=1.e-10)])
  return 1.0 / sum_var_inv


def get_weighted_mean(values, sigma):
  mean = 0.0
  if np.isclose(sum(values), 0.0):
    return mean
  for v, s in zip(values, sigma):
    if not np.isclose(v, 0.0):
      mean += v / (s * s)
  return mean * get_variance(sigma)


def average_data_item(item, limits):
  if range(len(limits)) == limits:
    # Equidistant values, no averaging necessary
    return item
  new_y = []
  new_y_err = []
  for i in range(len(limits)):
    if i < len(limits) - 1:
      l_low = limits[i]
      l_high = limits[i + 1] - 1
    else:
      l_low = limits[i]
      l_high = len(item[1][0]) - 1
    if l_low == l_high:
      # There is only one point for this x-value. Nothing to average over.
      new_y_err.append(item[1][2][l_low])
      new_y.append(item[1][1][l_low])
    else:
      new_y_err.append(np.sqrt(get_variance(item[1][2][l_low:l_high])))
      new_y.append(get_weighted_mean(item[1][1][l_low:l_high],
         item[1][2][l_low:l_high]))
  item = (item[0], np.array([item[1][0][limits], np.array(new_y),
          np.array(new_y_err)]))
  return item


def average_copies(data):
  for data_index, item in enumerate(data):
    limits = [0]
    current_x = item[1][0][0]
    for index, x, in enumerate(item[1][0]):
      if x != current_x:
        limits.append(index)
        current_x = x
    data[data_index] = average_data_item(data[data_index], limits)
  return data


class Scan_all():
  def __init__(self, input_lsts):
    if any([type(il) != list for il in input_lsts]):
      raise TypeError("Wrong input. Need a list of lists")
    self.dimension = len(input_lsts)
    self.lengths = [len(il) for il in input_lsts]
    self.values = input_lsts
    self.index_vec = [0 for _ in input_lsts]
    self.index_vec[0] = -1

  def __str__(self):
    string = 'Scanner:\n'
    string += ' dimension: ' + str(self.dimension)
    string += ' lengths:   ' + str(self.lengths)
    string += ' values:    ' + str(self.values)
    string += ' index_vec: ' + str(self.index_vec)
    return string

  def __iter__(self):
    return self

  # -> -> -> -> -\
  # \> -> -> -> -\
  # \> -> -> -> X
  def next(self):
    self.index_vec[0] += 1      # move along chain
    for k in range(self.dimension):
      over_flow = self.index_vec[k] == self.lengths[k]
      if over_flow:
        self.reset_and_move_to_next_chain(k)
    return [self.values[d][idx] for d, idx in enumerate(self.index_vec)]

  def reset_and_move_to_next_chain(self, k):
    self.index_vec[k] = 0
    if k + 1 < self.dimension:
      self.index_vec[k + 1] += 1
    else:
      raise StopIteration


@nt.raises(TypeError)
def test_scan_all_fail():
  test_input = [0.1, 0.2]
  scanner = Scan_all(test_input)
  for s in scanner:
    pass


def test_scan_all():
  test_input = [[1, 2]]
  scanner = Scan_all(test_input)
  expectation = [[1], [2]]
  for (s, e) in zip(scanner, expectation):
    nt.eq_(s, e)

  test_input = [[1, 2], ['a', 'b', 'c']]
  scanner = Scan_all(test_input)
  expectation = [[1, 'a'], [2, 'a'], [1, 'b'], [2, 'b'], [1, 'c'], [2, 'c']]
  for (s, e) in zip(scanner, expectation):
    nt.eq_(s, e)

  test_input = [[1, 2], ['a', 'b', 'c'], [0.1, 0.2]]
  scanner = Scan_all(test_input)
  expectation = [[1, 'a', 0.1], [2, 'a', 0.1], [1, 'b', 0.1],
                 [2, 'b', 0.1], [1, 'c', 0.1], [2, 'c', 0.1],
                 [1, 'a', 0.2], [2, 'a', 0.2], [1, 'b', 0.2],
                 [2, 'b', 0.2], [1, 'c', 0.2], [2, 'c', 0.2]]
  for (s, e) in zip(scanner, expectation):
    nt.eq_(s, e)


class Combiner():
  def __init__(self, x_generators, y_generators, lengths,
      yerr_generators=None, error_func=None, operation=lambda x: x):
    self.invalid = False
    self.yerrs = yerr_generators is not None
    self.next_x_values = 0
    self.next_y_values = 0
    self.next_yerr_values = 0
    self.x_generators = x_generators
    self.y_generators = y_generators
    self.yerr_generators = yerr_generators
    self.error_func = error_func
    self.operation = operation
    self.max_length = max(lengths)
    self.idx = 0
    self.x_arr = np.zeros(self.max_length)
    self.y_arr = np.zeros([self.max_length, len(self.y_generators)])
    if self.yerrs:
      self.yerr_arr = np.zeros([self.max_length, len(self.yerr_generators)])

  def save(self):
    if not self.invalid:
      self.x_arr[self.idx] = self.next_x_values[0]
      yval = self.operation(self.next_y_values)
      if np.size(yval) == 1:
        self.y_arr[self.idx, 0] = self.operation(self.next_y_values)
      else:
        self.y_arr[self.idx, :] = self.operation(self.next_y_values)
      if self.yerrs:
        self.yerr_arr[self.idx, :] = self.error_func(self)
      self.idx += 1

  def get_next_if_valid(self):
    if not self.invalid:
      self.next_x_values = [g.next() for g in self.x_generators]
      self.next_y_values = [g.next() for g in self.y_generators]
      if self.yerrs:
        self.next_yerr_values = [g.next() for g in self.yerr_generators]

  def skip_until_equal_x(self, idx, max_x):
    while True:
      next_x = self.x_generators[idx].next()
      next_y = self.y_generators[idx].next()
      if self.yerrs:
        next_yerr = self.yerr_generators[idx].next()
      if next_x >= max_x:
        self.next_x_values[idx] = next_x
        self.next_y_values[idx] = next_y
        if self.yerrs:
          self.next_yerr_values[idx] = next_yerr
        if np.isclose(next_x, max_x):
          self.invalid = False
        if next_x > max_x:
          self.invalid = True
        break

  def fetch_next(self):
    self.get_next_if_valid()
    if self.different_x_values():
      max_x = max(self.next_x_values)
      for idx, x in enumerate(self.next_x_values):
        if x < max_x:
          self.skip_until_equal_x(idx, max_x)

  def different_x_values(self):
    last_x = self.next_x_values[0]
    for x in self.next_x_values:
      if np.isclose(x, last_x):
        last_x = x
      else:
        return True
    return False

  # y_arr = [data_running, different_types]
  def get_all(self):
    try:
      while True:
        self.fetch_next()
        self.save()
    except StopIteration:
      self.x_arr = np.trim_zeros(self.x_arr)
      if np.all(self.y_arr[:, 1] == 0.):
        self.y_arr = self.y_arr[0:len(self.x_arr), 0]
      else:
        self.y_arr.resize(len(self.x_arr), np.shape(self.y_arr)[1])
        self.y_arr = self.y_arr.transpose()
      if self.yerrs:
        self.yerr_arr.resize(len(self.x_arr), np.shape(self.yerr_arr)[1])
        self.yerr_arr = self.yerr_arr.transpose()
        if self.yerr_arr.shape[0] == 1:
          self.yerr_arr = self.yerr_arr[0]
        return self.x_arr, self.y_arr, self.yerr_arr
      else:
        return self.x_arr, self.y_arr


def test_build_sum():
  test_file = 'test_build_sum.dat'
  test_file2 = 'test_build_sum2.dat'
  with open(test_file, 'w') as t:
    t.write('1. .1 .01\n')
    t.write('2. .2 .02\n')
  with open(test_file2, 'w') as t:
    t.write('1. .2 .02\n')
    t.write('2. .1 .01\n')
  files = [test_file, test_file2]
  data = [(filename, np.loadtxt(filename, unpack=True)) for filename in files]
  indices = [0, 1]
  combined_x, combined_y, combined_yerr = build_sum(data, indices)
  np.testing.assert_allclose(combined_x, np.array([1., 2.]))
  np.testing.assert_allclose(combined_y, np.array([.3, .3]))
  np.testing.assert_allclose(combined_yerr,
    np.array([np.sqrt(0.01**2 + 0.02**2), np.sqrt(0.02**2 + 0.01**2)]))

  with open(test_file, 'w') as t:
    t.write('1. .1 .01\n')
    t.write('2. .2 .02\n')
  with open(test_file2, 'w') as t:
    t.write('2. .2 .02\n')
    t.write('3. .1 .01\n')
  files = [test_file, test_file2]
  data = [(filename, np.loadtxt(filename, unpack=True)) for filename in files]
  indices = [0, 1]
  combined_x, combined_y, combined_yerr = build_sum(data, indices)
  np.testing.assert_allclose(combined_x, np.array([2.]))
  np.testing.assert_allclose(combined_y, np.array([.4]))
  os.remove(test_file)
  os.remove(test_file2)


def get_data_index(data, name):
  if '.dat' not in name:
    search_name = name + '.dat'
  else:
    search_name = name
  for i, d in enumerate(data):
    if search_name in d[0]:
      return i
  return -1


def apply_transforms(data, plot_json):
  transforms = plot_json.get('transforms', [])
  for transform in transforms:
    for action in transform:
      if action["type"] == "scalings":
         data = build_scaled(data, action)
      elif action["type"] == "smooth":
         data = build_smooth(data, action)
      elif action["type"] == "fits":
         data = build_fits(data, action)
      elif action["type"] == "binary_function":
         data = build_binary_function(data, action)
  return data


def test_apply_transforms():
  plot_json = {'transforms': [
      [{'type': 'binary_function'}]
  ]}
  data = []
  data = apply_transforms(data, plot_json)
  plot_json = {'transforms': [
      [{'type': 'binary_function'}, {'type': 'smooth'}]
  ]}
  data = []
  # data = apply_transforms(data, plot_json)

try:
  import include  # NOQA
  print "Including custom include.py file"
except ImportError:
  print "Did not find a custom include.py file"


def execute_defined_functions(data, plot_json):
  functions = plot_json.get("functions", None)
  if functions is not None:
    expression = functions['expression']
    exec('\n'.join(expression))
    for func in functions['to_evaluate']:
      entry = eval(func + '()')
      entry = (get_name({}, entry[0]), entry[1])
      print 'Executed ', func, 'and appended it under the tag', entry[0]
      data.append(entry)
  return data


def load_and_clean_files(files, plot_json=None):
  data = [(filename, np.loadtxt(filename, unpack=True)) for filename in files]
  data = remove_empty_data(data)
  data = sort_data(data)
  data = average_copies(data)
  data = build_nlo_sums(data)
  if plot_json is not None:
    data = execute_defined_functions(data, plot_json)
    data = apply_transforms(data, plot_json)
  data = remove_empty_data(data)
  return data


def smooth_data_sg(x_values, y_values, window_size=0, poly_order=3):
  # This filter does not change the x_values
  smoothed_x = x_values
  if window_size > 0:
    ws = window_size
  else:
    # Window size not specified. Use maximal allowed value.
    ws = len(y_values)
  # Note that the window size must be odd.
  if ws % 2 == 0:
    print colored('window size is not odd. Reduce by one.', 'yellow')
    ws -= 1
  try:
    smoothed_y = savgol_filter(y_values, ws, poly_order)
    return smoothed_x, smoothed_y
  except:
    if ws <= poly_order:
      print colored('SavGol-Filter failed because the window size is smaller \
        than the degree of the polynomial: ', 'red')
      print 'Given window size (minus 1 if even): ', ws
      print 'Polynomial degree: ', poly_order
    elif ws > len(y_values):
      print colored('SavGol-Filter failed because the window size is larger \
        than the total number of sampling points: ', 'red')
      print 'Given window size (minus 1 if even): ', ws
      print 'Number of sampling points: ', len(y_values)
    else:
      print colored('SavGol-Filter failed, but the reason could not be identified!',
        'red')
    print 'No Smoothing has been performed!'
    return x_values, y_values


#  TODO: (bcn 2016-08-16) is this art or can it go?
def smooth_data_internal(x_values, y_values, delta):
  smoothed_x = []
  smoothed_y = []
  x_mean = 0
  y_mean = 0
  n = 0
  x_left = x_values[0]
  for j, x in enumerate(x_values):
    x_right = x
    n += 1
    if abs(x_right - x_left) <= delta:
      x_mean += (x - x_mean) / n
      y_mean += (y_values[j] - y_mean) / n
    else:
      smoothed_x.append(x_mean)
      smoothed_y.append(y_mean)
      x_left = x
      n = 1
      x_mean = x
      y_mean = y_values[j]
  return smoothed_x, smoothed_y


def build_scaled(data, scale_dict):
  if scale_dict is None:
    return data
  scale_data = get_associated_plot_data(data, scale_dict)
  for data_of_a_scaling, scale in zip(scale_data, scale_dict):
    scale_by_value = scale.get('scale_by_value', None)
    scale_by_point = scale.get('scale_by_point', None)
    scale_by_x = scale.get('scale_by_x', None)
    for this_data in data_of_a_scaling:
      scaled_name = this_data[0].replace('.dat', '_scale.dat')
      for sc, sc_func in zip([scale_by_value, scale_by_point, scale_by_x],
          [add_scaled_by_value, add_scaled_by_point, add_scaled_by_x]):
        if sc is not None:
          this_scale_data = sc_func(sc, this_data)
          if this_scale_data is not None:
            print 'Appending ' + scaled_name
            data.append((scaled_name, this_scale_data))
  return data


def add_scaled_by_point(scale_by_point, this_data):
  x = this_data[1][0]
  scale_by_point = float(scale_by_point)
  index = np.where(np.isclose(x, scale_by_point))
  #  TODO: (bcn 2016-08-16) index[0] ?
  if (len(index[0]) == 0):
    print 'Cannot scale w.r.t. ' + str(scale_by_point) + '. Not in data!'
    return None
  elif(len(index[0]) > 1):
    print 'Cannot scale w.r.t. ' + str(scale_by_point) + '. Not uniqe!'
    print 'You have the same xvalue more than once in your data. It might be broken!'
    return None
  else:
    scale_value = this_data[1][1][index[0][0]]
    new_y = this_data[1][1] / scale_value
    try:
      new_y_err = this_data[1][2] / scale_value
      return np.array((x, new_y, new_y_err))
    except IndexError:
      return np.array((x, new_y))


def add_scaled_by_x(scale_by_x, this_data):
  x = this_data[1][0]
  y = this_data[1][1]
  if len(x) != len(y):
    print 'Cannot scale by x: x and y array have different lengths!'
    return None
  new_y = this_data[1][1] * pow(this_data[1][0], scale_by_x)
  try:
    new_y_err = this_data[1][2] * pow(this_data[1][0], scale_by_x)
    return np.array((x, new_y, new_y_err))
  except IndexError:
    return np.array((x, new_y))


def add_scaled_by_value(scale_by_value, this_data):
  x = this_data[1][0]
  scale_by_value = float(scale_by_value)
  new_y = this_data[1][1] / scale_by_value
  try:
    new_y_err = this_data[1][2] / scale_by_value
    return np.array((x, new_y, new_y_err))
  except IndexError:
    return np.array((x, new_y))
