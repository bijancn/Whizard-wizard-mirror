import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib._cm import cubehelix
from matplotlib.ticker import AutoMinorLocator
import matplotlib.gridspec as gridspec
import data_utils
from functools import partial
from utils import mkdirs
import fit_utils

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

# Valid legend locations
# right         # center left   # upper right    # lower right   # best
# center        # lower left    # center right   # upper left    # upper center
# lower center


class Plotter(object):
  def __init__(self):
    self.title_notset = True
    self.layout_notset = True

  # TODO: (bcn 2016-05-03) legend_outside seems broken with ratio plot
  def setfig(self, ax, xmin, xmax, ymin, ymax, xlabel, ylabel,
      title=None, xlog=False, ylog=False, xminors=False, yminors=False,
      n_minors=5, n_majors=6, xticks=None, yticks=None, puff=0.05,
      legend_location='best',
      legend_columns=1, legend_outside=False, height_shrinker=0.80,
      legend_hide=False, legend_ordering=[], ax1=None, ylabel1=None,
      ymin1=None, ymax1=None, n_majors1=None):
    # label axes and set ranges and scales
    if xlabel is not None:
      if ax1 is None:
        ax.set_xlabel(xlabel)
      else:
        ax1.set_xlabel(xlabel)
    if ylabel is not None:
      ax.set_ylabel(ylabel)
      if ylabel1 is not None and ax1 is not None:
        ax1.set_ylabel(ylabel1)
    _set_puffed_scale(puff, xmax, xmin, xlog, ax.set_xlim, ax.set_xscale)
    _set_puffed_scale(puff, ymax, ymin, ylog, ax.set_ylim, ax.set_yscale)
    if ymin1 is not None and ax1 is not None:
      _set_puffed_scale(puff, ymax1, ymin1, False, ax1.set_ylim, ax1.set_yscale)

    # title (ensuring no double set)
    if title is not None and self.title_notset:
      plt.suptitle(title, y=0.99)
      self.title_notset = False

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

    # major ticks
    if xticks is None:
      if xlog:
        xticks = np.logspace(math.log10(xmin), math.log10(xmax), num=n_majors)
      else:
        xticks = np.linspace(xmin, xmax, n_majors)
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(xt) for xt in xticks])
    if yticks is None:
      if ylog:
        yticks = np.logspace(math.log10(ymin), math.log10(ymax), num=n_majors)
      else:
        yticks = np.linspace(ymin, ymax, n_majors)
      if ymin1 is not None and ymax1 is not None and ax1 is not None:
        if n_majors1 is None:
          n_majors1 = n_majors
        yticks1 = np.linspace(ymin1, ymax1, n_majors1)
        ax1.set_yticks(yticks1)
    ax.set_yticks(yticks)

    # minor ticks are auto-set to n_minors if requested
    if xminors:
      if xlog:
        ax.set_xscale('log', subsx=[2, 3, 4, 5, 6, 7, 8, 9])
      else:
        minorLocator = AutoMinorLocator(n_minors)
        ax.xaxis.set_minor_locator(minorLocator)
    if yminors:
      if ylog:
        ax.set_yscale('log', subsy=[2, 3, 4, 5, 6, 7, 8, 9])
      else:
        minorLocator = AutoMinorLocator(n_minors)
        ax.yaxis.set_minor_locator(minorLocator)
        if ax1 is not None:
          ax1.yaxis.set_minor_locator(minorLocator)
    # TODO: (bcn 2016-03-16) minors are not disabled in log plot

    # legend
    if not legend_hide:
      handles, labels = ax.get_legend_handles_labels()
      # reorder if fitting sequence is given
      if len(legend_ordering) == len(handles):
        handles = map(handles.__getitem__, legend_ordering)
        labels = map(labels.__getitem__, legend_ordering)
      if legend_outside:
        # Shrink current axis's height by (1.0-height_shrinker) on the bottom
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * (1.0 - height_shrinker),
                         box.width, box.height * height_shrinker])
        # Put a legend below current axis
        ax.legend(handles, labels, loc='upper center',
            bbox_to_anchor=(0.5, -0.1),
            fancybox=False, ncol=legend_columns)
      else:
        ax.legend(handles, labels, loc=legend_location,
                  fancybox=False, ncol=legend_columns)


def check_for_all_sets(found_lines, wanted_lines):
  if len(found_lines) < len(wanted_lines):
    print 'Did not find all sets: But only ', len(found_lines), \
          ' out of ', len(wanted_lines)
    found_labels = [lbl[0] for lbl in found_lines]
    for l in wanted_lines:
      if not any([l == os.path.basename(label).replace('.dat', '') for
                 label in found_labels]):
        print l, ' not found!'
    print 'The available labels are: ', found_labels
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


def combined_plot(base_line, ax, ax1, x, y, *args, **kwargs):
  ax.plot(x, y, *args, **kwargs)
  comb = data_utils.normalize(base_line, x, y)
  ax1.plot(comb[0], comb[1], *args, **kwargs)


def combined_errorbar(base_line, ax, ax1, x, y, yerr=None, **kwargs):
  ax.errorbar(x, y, yerr=yerr, **kwargs)
  comb = data_utils.normalize(base_line, x, y, yerr=yerr)
  ax1.errorbar(comb[0], comb[1], yerr=comb[2], **kwargs)


def combined_fill_between(base_line, ax, ax1, x, ymin, ymax, *args, **kwargs):
  ax.fill_between(x, ymin, ymax, *args, **kwargs)
  comb = data_utils.normalize(base_line, x, ymin, yerr=ymax)
  ax1.fill_between(comb[0], comb[1], comb[2][0], *args, **kwargs)


def fit_plot(ax, x, y, xmin, xmax, degree, *args, **kwargs):
  fit_x, fit_y = fit_utils.fit_polynomial(x, y, xmin, xmax, degree)
  ax.plot(fit_x, fit_y, *args, **kwargs)


def smooth_plot(ax, x, y, delta, *args, **kwargs):
  smooth_x, smooth_y = data_utils.smooth_data(x, y, delta)
  ax.plot(smooth_x, smooth_y, *args, **kwargs)


def get_name(line):
  try:
    folder = line.get('folder', '.')
  except AttributeError:
    print 'lines and bands interface has changed:' + \
          'Please give an object with name instead of ' + line
  else:
    path = os.path.abspath(os.path.join(folder, 'scan-results', line.get('name', None)))
    return path


def get_associated_plot_data(data, special):
  special_data = []
  list_of_lists = [s.get('data', []) for s in special]
  for lbl_list in list_of_lists:
    this_special_data = []
    for lbl in lbl_list:
      this_special_data += [d for d in data
          if get_name(lbl) == d[0].replace('.dat', '')]
      special_data += [this_special_data]
  return special_data


def plot(plot_dict, data, pic_path='./', plot_extra=None, range_decider=None,
    label_decider=None, legend_decider=None, marker_decider=None,
    linestyle_decider=None, pretty_label=None, set_extra_settings=None,
    output_file=None):
  """
  data: [(identifier_string, numpy_array),...] where numpy_array has the columns
        x, y and optionally yerror
  """
  mkdirs(pic_path)
  title = plot_dict.get('title', 'plot')
  line_data = []
  lines = plot_dict.get('lines', [])
  for line in lines:
    line_data += [d for d in data if get_name(line) == d[0].replace('.dat', '')]
  bands = plot_dict.get('bands', [])
  band_data = get_associated_plot_data(data, bands)
  fits = plot_dict.get('fits', [])
  fit_data = get_associated_plot_data(data, fits)
  smooths = plot_dict.get('smooth', [])
  smooth_data = get_associated_plot_data(data, smooths)
  n_objects = len(line_data) + len(band_data) + len(fit_data) + len(smooth_data)
  many_labels = n_objects > 6
  check_for_all_sets(line_data, lines)
  # check_for_all_sets(band_data, band_lst)
  if n_objects == 0:
    print 'You selected no lines or bands. Not building: ' + title
    return
  try:
    size = (plot_dict['xpagelength'], plot_dict['ypagelength'])
  except KeyError:
    size = (9, 9) if many_labels else (9, 7.5)
  ratio_dict = plot_dict.get('ratio', None)
  if ratio_dict is not None:
    base_line = line_data[0][1]
    fig = plt.figure(figsize=size)
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    ax = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex=ax)
    ylabel1 = ratio_dict.get('ylabel', 'ratio')
    this_errorbar = partial(partial(partial(combined_errorbar, base_line), ax), ax1)
    this_plot = partial(partial(partial(combined_plot, base_line), ax), ax1)
    this_fill_between = partial(partial(partial(combined_fill_between,
      base_line), ax), ax1)
  else:
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(1, 1, 1)
    ax1 = None
    this_plot = ax.plot
    this_errorbar = ax.errorbar
    this_fill_between = ax.fill_between
    ylabel1 = None
  if len(fit_data) > 0:
    this_fit_plot = partial(fit_plot, ax)
  if len(smooth_data) > 0:
    this_smooth_plot = partial(smooth_plot, ax)
  if plot_extra is not None:
    ax = plot_extra(ax, title)
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
      # max([np.amax(d[1][1] / base_line) for d in all_data])
      # min([np.amin(d[1][1] / base_line) for d in all_data])
      n_majors1 = ratio_dict.get('nmajors', None)
    else:
      n_majors1 = None
  if label_decider is not None:
    xlabel, ylabel = label_decider(title)
  else:
    xlabel, ylabel = (plot_dict.get('xlabel', 'x'), plot_dict.get('ylabel', 'y'))
  xlog, ylog = (plot_dict.get('xlog', False), plot_dict.get('ylog', False))
  xminors, yminors = (plot_dict.get('xminors', False), plot_dict.get('yminors', False))
  decide_or_get = partial(decide_if_not_none, plot_dict)
  legend_location = decide_or_get(legend_decider, 'legend_location', 'best', title)
  if set_extra_settings is not None:
    ax = set_extra_settings(ax, title)
  pl = Plotter()
  i = 0
  global_opacity = plot_dict.get('opacity', 0.3)
  for data_of_a_band, band, color in zip(band_data, bands, colors):
    label = band.get('label', get_label(band, title, pretty_label=pretty_label))
    opacity = band.get('opacity', global_opacity)
    color = band.get('color', color)
    list_of_y_arrays = [db[1][1] for db in data_of_a_band]
    list_of_x_arrays = [db[1][0] for db in data_of_a_band]
    combined_x, list_of_y_arrays = data_utils.remove_uncommon(list_of_x_arrays,
        list_of_y_arrays)
    y_array = np.vstack(tuple(list_of_y_arrays))
    this_fill_between(combined_x, np.amin(y_array, axis=0), np.amax(y_array, axis=0),
        color=color, label=label, alpha=opacity)
  for td, line, color in zip(line_data, lines, colors):
    filename, d = td[0], td[1]
    label = get_label(line, title, filename=filename, pretty_label=pretty_label)
    # linestyle = decide_or_get(linestyle_decider, 'linestyle', None, filename, title)
    linestyle = decide_if_not_none(line, linestyle_decider, 'linestyle', 'solid',
        filename, title)
    c = line.get('color', color)
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
      if marker_decider is not None:
        marker = marker_decider(filename, title)
      else:
        marker = plot_dict.get('marker', '+')
      if len(d) > 2:
        this_errorbar(d[0], d[1], fmt=marker, yerr=d[2], color=c, label=label)
      else:
        this_errorbar(d[0], d[1], fmt=marker, color=c, label=label)
    if plot_dict.get('generate_animated', False):
      i += 1
      pl.setfig(ax, title=None,
                xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
                xminors=xminors, yminors=yminors,
                xlabel=xlabel,
                ylabel=ylabel, ylog=ylog, xlog=xlog,
                legend_outside=many_labels, height_shrinker=0.70,
                legend_location=legend_location,
                legend_hide=False, ax1=ax1, ylabel1=ylabel1, ymin1=ymin1,
                ymax1=ymax1, n_majors1=n_majors1)
      fig.savefig(os.path.join(pic_path, title + '-' + str(i) + '.pdf'),
                  dpi=fig.dpi)
  for data_of_a_fit, fit, color in zip(fit_data, fits, colors):
    label = fit.get('label', get_label(fit, title, pretty_label=pretty_label))
    color = fit.get('color', color)
    linestyle = decide_if_not_none(fit, linestyle_decider, 'linestyle', 'solid',
        data_of_a_fit[0][0], title)
    x = data_of_a_fit[0][1][0]
    y = data_of_a_fit[0][1][1]
    xmin = decide_if_not_none(fit, None, 'extrapolation_minus', min(x),
        data_of_a_fit[0][0], title)
    xmax = decide_if_not_none(fit, None, 'extrapolation_plus', max(x),
        data_of_a_fit[0][0], title)
    degree = decide_if_not_none(fit, None, 'fit_degree', -1,
        data_of_a_fit[0][0], title)
    if degree < 0:
      print 'You have not specified the degree of the polynomial to be fitted. '
      print 'Going to fit a line!'
      degree = 1
    this_fit_plot(x, y, xmin, xmax, degree, color=color,
      label=label, linestyle=linestyle)
  for data_of_a_smooth, smooth, color in zip(smooth_data, smooths, colors):
    label = smooth.get('label', get_label(smooth, title, pretty_label=pretty_label))
    color = smooth.get('color', color)
    linestyle = decide_if_not_none(smooth, linestyle_decider, 'linestyle', 'solid',
       data_of_a_smooth[0][0], title)
    delta = smooth.get('interval_size', 0)
    this_smooth_plot(data_of_a_smooth[0][1][0], data_of_a_smooth[0][1][1],
      delta, color=color, label=label, linestyle=linestyle)

  xticks = plot_dict.get('xticks', None)
  yticks = plot_dict.get('yticks', None)
  pl.setfig(ax, title=title,
            xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
            xminors=xminors, yminors=yminors,
            xlabel=xlabel,
            ylabel=ylabel, ylog=ylog, xlog=xlog,
            xticks=xticks, yticks=yticks,
            legend_outside=many_labels, height_shrinker=0.70,
            legend_location=legend_location, ax1=ax1, ylabel1=ylabel1,
            ymin1=ymin1, ymax1=ymax1, n_majors1=n_majors1)
  if output_file is not None:
    # We do not want to have to remember whether the ending has to be supplied
    if output_file.endswith('.pdf'):
      out_file = output_file
    else:
      out_file = output_file + '.pdf'
  else:
    out_file = title + '.pdf'
  print 'Writing to output: ', os.path.join(pic_path, out_file)
  fig.savefig(os.path.join(pic_path, out_file),
              dpi=fig.dpi)
  plt.close(fig)


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
