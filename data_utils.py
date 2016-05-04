import numpy as np
import nose.tools as nt
import os


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
    x = item[1][0]
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


def build_nlo_sums(data):
  for index, item in enumerate(data):
    if '_Born' in item[0]:
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
      print 'Appending ' + combined_name + ' to data'
      data.append((combined_name, array))
  return data


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
  x_gens = [(xx for xx in x), (xx for xx in base_line[0])]
  y_gens = [(yy for yy in y), (yy for yy in base_line[1])]
  lengths = [len(array) for array in [x, base_line[0]]]
  divide = lambda lst: reduce(lambda x, y: x / y, lst)
  if yerr is not None:
    # TODO: (bcn 2016-05-02) we should actually give the error of the base_line as well
    yerr_gen = (yyerr for yyerr in yerr)
    yerr_gens = [yerr_gen]
    error_func = lambda self: self.next_yerr_values / self.next_y_values[1]
  else:
    yerr_gens = None
    error_func = None
  combiner = Combiner(x_gens, y_gens, lengths,
      yerr_generators=yerr_gens, error_func=error_func, operation=divide)
  return combiner.get_all()


def test_normalize():
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


def combine_and_project(data, indices, operation, error_func):
  unpacked_data = [data[i][1] for i in indices]
  x_generators = [(value for value in array[0]) for array in unpacked_data]
  y_generators = [(value for value in array[1]) for array in unpacked_data]
  yerr_generators = [(value for value in array[2]) for array in unpacked_data]
  lengths = [len(array[0]) for array in unpacked_data]
  combiner = Combiner(x_generators, y_generators, lengths,
      yerr_generators=yerr_generators, error_func=error_func, operation=operation)
  return combiner.get_all()


def build_sum(data, indices):
  error_func = lambda self: np.sqrt(sum([yerr**2 for yerr in self.next_yerr_values]))
  return combine_and_project(data, indices, sum, error_func)


def build_ratio(data, indices):
  error_func = lambda self: np.sqrt(sum([yerr**2 for yerr in self.next_yerr_values]))
  raise Exception("This is not the correct error function. Please fix first.")
  return combine_and_project(data, indices, lambda x, y: x / y, error_func)


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

  def fetch_next(self):
    if not self.invalid:
      self.next_x_values = [g.next() for g in self.x_generators]
      self.next_y_values = [g.next() for g in self.y_generators]
      if self.yerrs:
        self.next_yerr_values = [g.next() for g in self.yerr_generators]
    different_x_values = len(set(self.next_x_values)) > 1
    if different_x_values:
      max_x = max(self.next_x_values)
      for idx, x in enumerate(self.next_x_values):
        if x < max_x:
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
              if next_x == max_x:
                self.invalid = False
              if next_x > max_x:
                self.invalid = True
              break

  # y_arr = [data_running, different_types]
  def get_all(self):
    try:
      while True:
        self.fetch_next()
        self.save()
    except StopIteration:
      self.x_arr = np.trim_zeros(self.x_arr)
      if np.all(self.y_arr[:, 1] == 0.):
        self.y_arr = np.trim_zeros(self.y_arr[:, 0])
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


def load_and_clean_files(files):
  print 'Loading data'
  data = [(filename, np.loadtxt(filename, unpack=True)) for filename in files]
  data = remove_empty_data(data)
  print 'Sorting data'
  data = sort_data(data)
  print 'Building NLO sums'
  data = build_nlo_sums(data)
  data = remove_empty_data(data)
  return data