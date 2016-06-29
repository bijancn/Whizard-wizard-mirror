import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib._cm import cubehelix
from matplotlib.ticker import AutoMinorLocator
import matplotlib.gridspec as gridspec
import data_utils
from data_utils import get_name
from functools import partial
from utils import mkdirs
try:
  import mpld3
except:
  mpld3 = None

colors = ['#EE3311',  # red
          '#3366FF',  # blue
          '#109618',  # green
          '#FF9900',  # orange
          '#80deea',  # cyan
          '#ab47bc',  # purple
          '#000000',  # black
          '#f06292',  # pink
          # '#cddc39',  # lime
          '#3f51b5'   # indigo
          # '#009688',  # teal
          ]

N_YMINORS_DEFAULT = 5
N_XMINORS_DEFAULT = 5
N_YMAJORS_DEFAULT = 6
N_XMAJORS_DEFAULT = 6


def set_labels(ax, ax1, xlabel, ylabel, ylabel1):
  if xlabel is not None:
    if ax1 is None:
      ax.set_xlabel(xlabel)
    else:
      ax1.set_xlabel(xlabel)
  if ylabel is not None:
    ax.set_ylabel(ylabel)
    if ylabel1 is not None and ax1 is not None:
      ax1.set_ylabel(ylabel1)


def set_major_ticks(ax, ax1, xticks, yticks, xmin, xmax, xmajors, ymin, ymax,
    ymajors, ymin1, ymax1, ymajors1, xlog, ylog):
  if xticks is None:
    if xlog:
      xticks = np.logspace(math.log10(xmin), math.log10(xmax), num=xmajors)
    else:
      xticks = np.linspace(xmin, xmax, xmajors)
  ax.set_xticks(xticks)
  ax.set_xticklabels([str(xt) for xt in xticks])
  if yticks is None:
    if ylog:
      yticks = np.logspace(math.log10(ymin), math.log10(ymax), num=ymajors)
    else:
      yticks = np.linspace(ymin, ymax, ymajors)
    if ymin1 is not None and ymax1 is not None and ax1 is not None:
      if ymajors1 is None:
        ymajors1 = ymajors
      yticks1 = np.linspace(ymin1, ymax1, ymajors1)
      ax1.set_yticks(yticks1)
  ax.set_yticks(yticks)


def set_minor_ticks(ax, ax1, xminors, yminors, xlog, ylog):
  # TODO: (bcn 2016-03-16) minors are not disabled in log plot
  if xminors > 0:
    if xlog:
      ax.set_xscale('log', subsx=[2, 3, 4, 5, 6, 7, 8, 9])
    else:
      minorLocator = AutoMinorLocator(xminors)
      ax.xaxis.set_minor_locator(minorLocator)
  if yminors > 0:
    if ylog:
      ax.set_yscale('log', subsy=[2, 3, 4, 5, 6, 7, 8, 9])
    else:
      minorLocator = AutoMinorLocator(yminors)
      ax.yaxis.set_minor_locator(minorLocator)
      if ax1 is not None:
        minorLocator = AutoMinorLocator(yminors)
        ax1.yaxis.set_minor_locator(minorLocator)


def set_legend(fig, ax, ax1, legend_ordering, legend_outside, height_shrinker,
    legend_columns, legend_location):
  handles, labels = ax.get_legend_handles_labels()
  # reorder if fitting sequence is given
  if len(legend_ordering) == len(handles):
    handles = map(handles.__getitem__, legend_ordering)
    labels = map(labels.__getitem__, legend_ordering)
  if legend_outside:
    # Shrink current axis's height by (1.0-height_shrinker) on the bottom
    if ax1 is None:
      box = ax.get_position()
      ax.set_position([box.x0, box.y0 + box.height * (1.0 - height_shrinker),
                       box.width, box.height * height_shrinker])
      # Put a legend below current axis
      ax.legend(handles, labels, loc='upper center',
          bbox_to_anchor=(0.5, -0.1),
          fancybox=False, ncol=legend_columns)
    else:
      box = ax.get_position()
      reduced_amount = box.height * (1.0 - height_shrinker)
      ax.set_position([box.x0, box.y0 + box.height * (1.0 - height_shrinker),
                       box.width, box.height * height_shrinker])
      box = ax1.get_position()
      ax1.set_position([box.x0, box.y0 + reduced_amount + box.height * (1.0 -
        height_shrinker), box.width, box.height * height_shrinker])
      # Put a legend below current axis (coordinates are relative to ax1)
      fig.legend(handles, labels, loc='lower center',
          bbox_to_anchor=(0.5, 0.0),
          fancybox=False, ncol=legend_columns)
  else:
    ax.legend(handles, labels, loc=legend_location,
              fancybox=False, ncol=legend_columns)


class Plotter(object):
  def __init__(self):
    self.title_notset = True
    self.layout_notset = True

  def set_layout(self):
    # tight layout with extra padding
    # pad : padding between the figure edge and the edges of subplots, as a
    #       fraction of the font-size
    # h_pad, w_pad : padding (height/width) between edges of adjacent subplots.
    #                Defaults to pad_inches
    # rect : if rect is given, it is interpreted as a rectangle
    #       (left, bottom, right, top) in the normalized figure coordinate that
    #       the whole subplots area (including labels) will fit into.
    #       Default is (0, 0, 1, 1)
    #       We set top to 0.96 to have space for title
    if self.layout_notset:
      plt.tight_layout(pad=0.5, rect=[0.04, 0.00, 1, 0.96])
      plt.subplots_adjust(hspace=0.01)
      self.layout_notset = False

  def setfig(self, fig, ax, xmin, xmax, ymin, ymax, xlabel, ylabel,
      title=None, xlog=False, ylog=False,
      xmajors=N_XMAJORS_DEFAULT, ymajors=N_YMAJORS_DEFAULT,
      xminors=0, yminors=0,
      xticks=None, yticks=None, puff=0.05,
      legend_location='best',
      legend_columns=1, legend_outside=False, height_shrinker=0.80,
      legend_hide=False, legend_ordering=[], ax1=None, ylabel1=None,
      ymin1=None, ymax1=None, ymajors1=None):
    set_labels(ax, ax1, xlabel, ylabel, ylabel1)
    _set_puffed_scale(puff, xmax, xmin, xlog, ax.set_xlim, ax.set_xscale)
    _set_puffed_scale(puff, ymax, ymin, ylog, ax.set_ylim, ax.set_yscale)
    if ymin1 is not None and ax1 is not None:
      _set_puffed_scale(puff, ymax1, ymin1, False, ax1.set_ylim, ax1.set_yscale)
    if title is not None and self.title_notset:
      plt.suptitle(title, y=0.99)
      self.title_notset = False
    self.set_layout()
    set_major_ticks(ax, ax1, xticks, yticks, xmin, xmax, xmajors, ymin, ymax,
        ymajors, ymin1, ymax1, ymajors1, xlog, ylog)
    set_minor_ticks(ax, ax1, xminors, yminors, xlog, ylog)
    if not legend_hide:
      set_legend(fig, ax, ax1, legend_ordering, legend_outside, height_shrinker,
          legend_columns, legend_location)


def check_for_all_sets(found_lines, wanted_lines):
  if len(found_lines) < len(wanted_lines):
    print 'Did not find all sets: But only ', len(found_lines), \
          ' out of ', len(wanted_lines)
    found_labels = [lbl[0] for lbl in found_lines]
    for l in wanted_lines:
      if not any([l['name'] == os.path.basename(label).replace('.dat', '') for
                 label in found_labels]):
        print l, ' not found!'
    print 'The available labels are: ', found_labels
    print 'The wanted labels are: ', wanted_lines
    sys.exit(1)


def decide_if_not_none(dictionary, decider, thing_to_set, default, *args):
  try:
    return dictionary[thing_to_set]
  except (KeyError, TypeError):
    if decider is not None:
      return decider(*args)
    else:
      return default


def get_label(object_dict, title, filename=None, pretty_label=None):
  label = ''
  if filename is not None:
    default = os.path.basename(filename)
    label = decide_if_not_none(object_dict, pretty_label, 'label', default,
        filename, title).replace('_', '\_').replace('--', '_')
  return object_dict.get('label', label)


def combined_plot(ax, ax1, base_line, x, y, *args, **kwargs):
  ax.plot(x, y, *args, **kwargs)
  comb = data_utils.normalize(base_line, x, y)
  ax1.plot(comb[0], comb[1], *args, **kwargs)


def combined_errorbar(ax, ax1, base_line, x, y, yerr=None, **kwargs):
  ax.errorbar(x, y, yerr=yerr, **kwargs)
  comb = data_utils.normalize(base_line, x, y, yerr=yerr)
  if len(comb[0]) != len(comb[1]):
    raise Exception("normalize gave incoherent data: len(x) != len(y): " +
        str(len(comb[0])) + " != " + str(len(comb[1])))
  ax1.errorbar(comb[0], comb[1], yerr=comb[2], **kwargs)


def combined_fill_between(ax, ax1, base_line, x, ymin, ymax, *args, **kwargs):
  ax.fill_between(x, ymin, ymax, *args, **kwargs)
  comb = data_utils.normalize(base_line, x, ymin, yerr=ymax)
  ax1.fill_between(comb[0], comb[1], comb[2], *args, **kwargs)


def scale_data(item_data, items):
  for i_data, item in zip(item_data, items):
    scale_by_value = item.get('scale_by_value', 0)
    scale_by_point = item.get('scale_by_point', None)
    if scale_by_value > 0 and (scale_by_point is not None):
      print 'Cannot scale by a fixed value and with reference to a fixed point'
      print 'at the same time. Not building ' + item[0]
      return
    if scale_by_value > 0:
      i_data[1][1] /= scale_by_value
      i_data[1][2] /= scale_by_value
    if scale_by_point is not None:
      index = np.where(i_data[1][0] == scale_by_point)
      if (len(index[0]) == 0):
        print 'Cannot scale w.r.t.' + str(scale_by_point) + '. Not in data!'
        return
      elif(len(index[0]) > 1):
        print 'Cannot scale w.r.t.' + str(scale_by_point) + '. Not uniqe!'
        print 'You have the same xvalue more than once in your data. It might be broken!'
        return
      else:
        scale_value = i_data[1][1][index[0][0]]
        i_data[1][1] /= scale_value
        i_data[1][2] /= scale_value
  return item_data


def get_object_name(obj, is_fit):
  if not is_fit:
    return obj.get('name', '')
  else:
    fit_data = obj.get('data', None)
    if fit_data is not None:
      name = fit_data[0].get('name', '')
      if name is not '':
        name += '_fit'
    else:
      name = ''
    return name


# TODO: (bcn 2016-06-29) what was the idea for this? different base_lines? I
# solved this differently, so maybe this is redundant now
def insert_group_entry(groups, data, obj, is_fit=False):
  name = get_object_name(obj, is_fit)
  group = obj.get('baseline_group', -1)
  if group >= 0:
    index = data_utils.get_data_index(data, name)
    if obj.get('is_baseline', False):
      baseline_index = index
    else:
      baseline_index = -1
    if str(group) in groups:
      groups[str(group)][0].append(index)
      if baseline_index >= 0:
        if baseline_index == groups[str(group)][1]:
          # A baseline index has already been set. More than one
          # data set want to be baselines!
          print 'More than one baseline encountered! Please check plot.json.'
        else:
          groups[str(group)][1] = baseline_index
    else:
      groups[str(group)] = [[index], baseline_index]
  return groups


def create_baseline_groups(data, plot_dict):
  groups = {}
  for line in plot_dict.get('lines', []):
    groups = insert_group_entry(groups, data, line)
  for fit in plot_dict.get('fits', []):
    groups = insert_group_entry(groups, data, fit, is_fit=True)


def sanity_check(data):
  for dat in data:
    if type(dat[0]) is not str:
      print 'This is not an identifier_string:', dat[0]
      print 'Aborting'
      return False
    if type(dat[1]) is not np.ndarray:
      print 'This is not a numpy ndarray:', dat[1], 'in', dat[0]
      print 'Aborting'
      return False
    if len(dat[1].shape) != 2:
      print 'These are inconsistent shapes:', dat[1].shape, 'in', dat[0]
      print 'It should be (2, N) or (3, N). Aborting'
      return False
  return True


def setup_figure(plot_dict, ratio_dict, many_labels):
  try:
    size = (plot_dict['xpagelength'], plot_dict['ypagelength'])
  except KeyError:
    size = (9, 9) if many_labels else (9, 7.5)
  return plt.figure(figsize=size)


def setup_labels(label_decider, title, plot_dict, ratio_dict):
  label_kwargs = {}
  if label_decider is not None:
    label_kwargs['xlabel'], label_kwargs['ylabel'] = label_decider(title)
  else:
    label_kwargs['xlabel'] = plot_dict.get('xlabel', 'x')
    label_kwargs['ylabel'] = plot_dict.get('ylabel', 'y')
  if ratio_dict is not None:
    label_kwargs['ylabel1'] = ratio_dict.get('ylabel', 'ratio')
  else:
    label_kwargs['ylabel1'] = None
  return label_kwargs


def setup_ranges(range_decider, line_data, band_data, title,
    plot_dict, ratio_dict):
  ymin1, ymax1 = None, None
  if range_decider is not None:
    ymin, ymax, xmin, xmax = range_decider(line_data, title)
  else:
    try:
      flattened_band_data = reduce(lambda x, y: x + y, band_data)
    except TypeError:
      flattened_band_data = []
    all_data = line_data + flattened_band_data
    xmin = plot_dict.get('xmin', min([np.amin(d[1][0]) for d in all_data]))
    xmax = plot_dict.get('xmax', min([np.amax(d[1][0]) for d in all_data]))
    ymin = plot_dict.get('ymin', min([np.amin(d[1][1]) for d in all_data]))
    ymax = plot_dict.get('ymax', max([np.amax(d[1][1]) for d in all_data]))
    if ratio_dict is not None:
      ymax1 = ratio_dict.get('ymax', None)
      ymin1 = ratio_dict.get('ymin', None)
  fig_kwargs = {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax,
      'ymin1': ymin1, 'ymax1': ymax1}
  return fig_kwargs


def plot_band(data_of_a_band, band, color, title, global_opacity, pretty_label,
  this_fill_between):
  label = get_label(band, title, pretty_label=pretty_label)
  opacity = band.get('opacity', global_opacity)
  color = band.get('color', color)
  list_of_y_arrays = [db[1][1] for db in data_of_a_band]
  list_of_x_arrays = [db[1][0] for db in data_of_a_band]
  combined_x, list_of_y_arrays = data_utils.remove_uncommon(list_of_x_arrays,
      list_of_y_arrays)
  y_array = np.vstack(tuple(list_of_y_arrays))
  this_fill_between(combined_x, np.amin(y_array, axis=0), np.amax(y_array, axis=0),
      color=color, label=label, alpha=opacity)


def plot_line(ldata, line, color, title, pretty_label, linestyle_decider,
    marker_decider, this_errorbar, this_plot, this_fill_between, ax,
    global_opacity, plotter):
  filename, d = ldata[0], ldata[1]
  label = get_label(line, title, pretty_label=pretty_label, filename=filename)
  c = line.get('color', color)
  if line.get('hide_label', False):
    label = None
  linestyle = decide_if_not_none(line, linestyle_decider, 'linestyle', 'solid',
      filename, title)
  if linestyle == 'banded':
    if len(d) > 2:
      this_fill_between(d[0], d[1] - d[2], d[1] + d[2],
        color=c, label=label, alpha=global_opacity)
    else:
      raise Exception("You have to supply errors for banded linestyle")
  elif linestyle == 'scatter':
    # TODO: (bcn 2016-03-31) hacking in a ratio for now #notproud
    ax.scatter(d[0], d[1] / d[2], c=c, alpha=global_opacity, label=label, marker="+")
  elif linestyle == 'histogram':
    # TODO: (bcn 2016-03-31) hacking in a ratio for now #notproud
    nbins = 10
    n, _ = np.histogram(d[0], bins=nbins)
    sy, _ = np.histogram(d[0], bins=nbins, weights=d[1] / d[2])
    sy2, _ = np.histogram(d[0], bins=nbins, weights=d[1] / d[2] * d[1] / d[2])
    mean = sy / n
    std = np.sqrt(sy2 / n - mean * mean)
    plt.errorbar((_[1:] + _[:-1]) / 2, mean, yerr=std, ecolor=c, fmt="none",
        alpha=global_opacity)
    plt.hlines(mean, _[:-1], _[1:], label=label, colors=c)
  elif linestyle is not None and linestyle != "None":
    this_plot(d[0], d[1], color=c, label=label, linestyle=linestyle)
  else:
    marker = decide_if_not_none(line, marker_decider, 'marker', '+')
    if len(d) > 2:
      this_errorbar(d[0], d[1], fmt=marker, yerr=d[2], color=c, label=label)
    else:
      this_errorbar(d[0], d[1], fmt=marker, color=c, label=label)


def save_fig(fig, title, plot_dict, pic_path):
  output_file = plot_dict.get('output_file', '')
  if output_file is not '':
    # We do not want to have to remember whether the ending has to be supplied
    if output_file.endswith('.pdf'):
      out_file = output_file
    else:
      out_file = output_file + '.pdf'
  else:
    out_file = title + '.pdf'
  print 'Writing to output: ', out_file.replace('.pdf', '')
  out_path = os.path.join(pic_path, out_file).replace(' ', '_')
  strip_chars = ['(', ')', ',', ';']
  for sc in strip_chars:
    out_path = out_path.replace(sc, '')
  fig.savefig(out_path, dpi=fig.dpi)
  out_path = out_path.replace('.pdf', '.svg')
  fig.savefig(out_path, dpi=fig.dpi)
  if mpld3 is not None:
    out_path = out_path.replace('.svg', '.html')
    with open(out_path, 'w') as fileobj:
      mpld3.save_html(fig, fileobj, template_type='simple',
        mpld3_url='../mpld3.v0.2.js', d3_url='../d3.v3.min.js')
  plt.close(fig)


def select_data(data, plot_dict, title):
  valid = sanity_check(data)
  line_data = []
  lines = plot_dict.get('lines', [])
  for line in lines:
    line_data += [d for d in data if get_name(line) == d[0].replace('.dat', '')]
  line_data = scale_data(line_data, lines)
  bands = plot_dict.get('bands', [])
  band_data = data_utils.get_associated_plot_data(data, bands)
  fits = plot_dict.get('fits', [])
  fit_data = data_utils.get_associated_plot_data(data, fits)
  n_objects = len(line_data) + len(band_data) + len(fit_data)
  many_labels = n_objects > 6
  check_for_all_sets(line_data, lines)
  # check_for_all_sets(band_data, band_lst)
  if n_objects == 0:
    print 'You selected no lines or bands. Not building: ' + title
    valid = False
  return valid, line_data, band_data, fit_data, many_labels, lines, bands, fits


def setup_extra_kwargs(plot_dict, legend_decider, many_labels, title):
  extra_kwargs = {}
  extra_kwargs['height_shrinker'] = 0.70
  extra_kwargs['xlog'] = plot_dict.get('xlog', False)
  extra_kwargs['ylog'] = plot_dict.get('ylog', False)
  extra_kwargs['xminors'] = plot_dict.get('xminors', N_XMINORS_DEFAULT)
  extra_kwargs['yminors'] = plot_dict.get('yminors', N_YMINORS_DEFAULT)
  extra_kwargs['xticks'] = plot_dict.get('xticks', None)
  extra_kwargs['yticks'] = plot_dict.get('yticks', None)
  extra_kwargs['legend_outside'] = plot_dict.get('legend_outside', many_labels)
  extra_kwargs['legend_location'] = decide_if_not_none(plot_dict, legend_decider,
      'legend_location', 'best', title)
  return extra_kwargs


def setup_majors(plot_dict, ratio_dict):
  kwargs = {}
  kwargs['ymajors'] = plot_dict.get('ymajors', None)
  kwargs['xmajors'] = plot_dict.get('xmajors', None)
  if ratio_dict is not None:
    kwargs['ymajors1'] = ratio_dict.get('ymajors', None)
  else:
    kwargs['ymajors1'] = None
  return kwargs


def use_local_or_global_base_line(band_or_line, data, this_errorbar_func,
    this_plot_func, this_fill_between_func, global_base_line):
  base_line = band_or_line.get('base_line', None)
  if base_line is not None:
    this_base_line = [d for d in data
        if get_name(base_line) == d[0].replace('.dat', '')][0][1]
    this_errorbar = partial(this_errorbar_func, this_base_line)
    this_plot = partial(this_plot_func, this_base_line)
    this_fill_between = partial(this_fill_between_func, this_base_line)
  else:
    this_errorbar = partial(this_errorbar_func, global_base_line)
    this_plot = partial(this_plot_func, global_base_line)
    this_fill_between = partial(this_fill_between_func, global_base_line)
  return this_errorbar, this_plot, this_fill_between


def plot(plot_dict, data, pic_path='./', plot_extra=None, range_decider=None,
    label_decider=None, legend_decider=None, marker_decider=None,
    linestyle_decider=None, pretty_label=None, set_extra_settings=None):
  """
  data: [(identifier_string, numpy_array),...] where numpy_array has the columns
        x, y and optionally yerror
  """
  title = plot_dict.get('title', 'plot')
  mkdirs(pic_path)
  valid, line_data, band_data, fit_data, many_labels, lines, bands, fits = \
      select_data(data, plot_dict, title)
  if not valid:
    return
  # We are going to use this in the future
  # TODO: (bcn 2016-06-29) Really?
  # groups = create_baseline_groups(data, plot_dict)
  ratio_dict = plot_dict.get('ratio', None)
  fig_kwargs = setup_ranges(range_decider, line_data,
      band_data, title, plot_dict, ratio_dict)
  fig = setup_figure(plot_dict, ratio_dict, many_labels)
  if ratio_dict is not None:
    global_base_line = line_data[0][1]
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    ax = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex=ax)
    this_errorbar_func = partial(partial(combined_errorbar, ax), ax1)
    this_plot_func = partial(partial(combined_plot, ax), ax1)
    this_fill_between_func = partial(partial(combined_fill_between, ax), ax1)
    fig_kwargs['ax1'] = ax1
  else:
    ax = fig.add_subplot(1, 1, 1)
    this_plot = ax.plot
    this_errorbar = ax.errorbar
    this_fill_between = ax.fill_between
    fig_kwargs['ax1'] = None
  if plot_extra is not None:
    ax = plot_extra(ax, title)
  fig_kwargs.update(setup_majors(plot_dict, ratio_dict))
  fig_kwargs.update(setup_labels(label_decider, title, plot_dict, ratio_dict))
  fig_kwargs.update(setup_extra_kwargs(plot_dict, legend_decider, many_labels, title))
  if set_extra_settings is not None:
    ax = set_extra_settings(ax, title)
  plotter = Plotter()
  i = 0
  global_opacity = plot_dict.get('opacity', 0.3)
  for data_of_a_band, band, color in zip(band_data, bands, colors):
    if ratio_dict is not None:
      this_errorbar, this_plot, this_fill_between = \
          use_local_or_global_base_line(band, data, this_errorbar_func,
          this_plot_func, this_fill_between_func, global_base_line)
    plot_band(data_of_a_band, band, color, title, global_opacity, pretty_label,
        this_fill_between)
  for ldata, line, color in zip(line_data + fit_data, lines + fits, colors + colors):
    i += 1
    if ratio_dict is not None:
      this_errorbar, this_plot, this_fill_between = \
          use_local_or_global_base_line(line, data, this_errorbar_func,
          this_plot_func, this_fill_between_func, global_base_line)
    plot_line(ldata, line, color, title, pretty_label, linestyle_decider,
        marker_decider, this_errorbar, this_plot, this_fill_between, ax,
        global_opacity, plotter)
    if plot_dict.get('generate_animated', False):
      plotter.setfig(fig, ax, title=None, legend_hide=False, **fig_kwargs)
      fig.savefig(os.path.join(pic_path, title + '-' + str(i) + '.pdf'),
                  dpi=fig.dpi)
  plotter.setfig(fig, ax, title=title, **fig_kwargs)
  save_fig(fig, title, plot_dict, pic_path)


def get_linecolors_from_cubehelix(N, gamma=0.8, hue=3.0, rot=1.8, start=-0.30):
  """Return N colors from the cubehelix for plots
  """
  rgb_dict = cubehelix(h=hue, r=rot, gamma=gamma, s=start)
  brightness = np.linspace(0.0, 1.0, num=N, endpoint=False)
  rgb_list = [(rgb_dict['red'](b), rgb_dict['green'](b),
              rgb_dict['blue'](b)) for b in brightness]
  ret = [(_norm(a), _norm(b), _norm(c)) for a, b, c in rgb_list]
  return ret


def _set_puffed_scale(puff, smax, smin, slog, ax_set_slim, ax_set_sscale):
  if slog:
    puffs = puff * np.log(smax - smin)
    ax_set_slim(np.exp(np.log(smin) - puffs),
                np.exp(np.log(smax) + puffs))
    ax_set_sscale('log')
  else:
    puffx = puff * (smax - smin)
    ax_set_slim(smin - puffx, smax + puffx)


def _norm(x):
  if (x > 1.0):
    return 1.0
  if (x < 0.0):
    return 0.0
  return x
