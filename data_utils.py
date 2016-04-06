import numpy as np


def sort_data(data):
  for index, item in enumerate(data):
    try:
      x = item[1][0]
    except IndexError:
      print 'Ignoring empty data: ', data[index][0]
      del data[index]
    if x.size > 1:
      y = item[1][1]
      yerr = item[1][2]
      order = np.argsort(x)
      data[index] = (item[0], np.array((x[order], y[order], yerr[order])))
  return data


def build_nlo_sums(data):
  for index, item in enumerate(data):
    if '_Born' in item[0]:
      real_index = next((i for i, x in enumerate(data) if
        item[0].replace('_Born', '_Real') == x[0]))
      virtual_index = next((i for i, x in enumerate(data) if
        item[0].replace('_Born', '_Virtual') == x[0]))
      combined_x, combined_y, combined_yerr = build_sum(data,
          [index, real_index, virtual_index])
      combined_name = item[0].replace('_Born', '')
      array = np.array((combined_x, combined_y, combined_yerr))
      data.append((combined_name, array))
  return data


def build_sum(data, indices):
  print 'building sum of: ', [data[i][0] for i in indices]
  unpacked_data = [data[i][1] for i in indices]
  x_generators = [(value for value in array[0]) for array in unpacked_data]
  y_generators = [(value for value in array[1]) for array in unpacked_data]
  yerr_generators = [(value for value in array[2]) for array in unpacked_data]
  # TODO: (bcn 2016-04-05) prealloc max size and then trim
  combined_x = np.empty(0)
  combined_y = np.empty(0)
  combined_yerr = np.empty(0)
  try:
    while True:
      next_x_values = [g.next() for g in x_generators]
      next_y_values = [g.next() for g in y_generators]
      next_yerr_values = [g.next() for g in yerr_generators]
      if len(set(next_x_values)) > 1:
        max_x = max(next_x_values)
        for idx, x in enumerate(next_x_values):
          if x < max_x:
            while True:
              next_x = x_generators[idx].next()
              next_y = y_generators[idx].next()
              next_yerr = yerr_generators[idx].next()
              if next_x == max_x:
                next_x_values[idx] = next_x
                next_y_values[idx] = next_y
                next_yerr_values[idx] = next_yerr
                break
      combined_x = np.append(combined_x, next_x_values[0])
      combined_y = np.append(combined_y, sum(next_y_values))
      combined_yerr = np.append(combined_yerr,
          np.sqrt(sum((yerr * yerr for yerr in next_yerr_values))))
  except StopIteration:
    pass
  return combined_x, combined_y, combined_yerr


def load_and_clean_files(files):
  print 'Loading data'
  data = [(filename, np.loadtxt(filename, unpack=True)) for filename in files]
  print 'Sorting data'
  data = sort_data(data)
  print 'Building NLO sums'
  data = build_nlo_sums(data)
  return data
