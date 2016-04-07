import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib._cm import cubehelix
from matplotlib.ticker import AutoMinorLocator
import matplotlib.gridspec as gridspec
from functools import partial
from utils import mkdirs

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


def get_label(title, filename=None, pretty_label=None, object_dict=None):
  if filename is not None:
    default = os.path.basename(filename)
    return decide_if_not_none(object_dict, pretty_label, 'label', default,
        filename, title).replace('_', '\_')
  else:
    return object_dict.get('label', '').replace('_', '\_')


def combined_plot(base_line, ax, ax1, x, y, *args, **kwargs):
  ax.plot(x, y, *args, **kwargs)
  ax1.plot(x, y / base_line, *args, **kwargs)


def combined_fill_between(base_line, ax, ax1, x, ymin, ymax, *args, **kwargs):
  ax.fill_between(x, ymin, ymax, *args, **kwargs)
  ax1.fill_between(x, ymin / base_line, ymax / base_line, *args, **kwargs)


def plot(plot_dict, data, pic_path='./', plot_extra=None, range_decider=None,
    label_decider=None, legend_decider=None, marker_decider=None,
    linestyle_decider=None, pretty_label=None, set_extra_settings=None):
  """
  data: [(identifier_string, numpy_array),...] where numpy_array has the columns
        x, y and optionally yerror
  """
  mkdirs(pic_path)
  title = plot_dict.get('title', 'plot')
  print 'Plotting ' + title
  line_data = []
  lines = plot_dict.get('lines', [])
  for lbl in lines:
    line_data += [d for d in data if lbl == os.path.basename(d[0]).replace('.dat', '')]
  bands = plot_dict.get('bands', [])
  band_data = []
  lst_of_band_lsts = [b.get('data', []) for b in bands]
  for lbl_lst in lst_of_band_lsts:
    this_band_data = []
    for lbl in lbl_lst:
      this_band_data += [d for d in data
          if lbl == os.path.basename(d[0]).replace('.dat', '')]
    band_data += [this_band_data]
  n_objects = len(line_data) + len(band_data)
  many_labels = n_objects > 6
  check_for_all_sets(line_data, lines)
  # check_for_all_sets(band_data, band_lst)
  if n_objects == 0:
    print 'You selected no lines or bands. Not building: ' + title
    return
  size = (9, 9) if many_labels else (9, 7.5)
  ratio_dict = plot_dict.get('ratio', None)
  if ratio_dict is not None:
    base_line = line_data[0][1][1]
    fig = plt.figure(figsize=size)
    gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
    ax = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex=ax)
    ylabel1 = ratio_dict.get('ylabel', 'ratio')
    this_plot = partial(partial(partial(combined_plot, base_line), ax), ax1)
    this_fill_between = partial(partial(partial(combined_fill_between,
      base_line), ax), ax1)
  else:
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(1, 1, 1)
    ax1 = None
    this_plot = ax.plot
    this_fill_between = ax.fill_between
    ylabel1 = None
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
      ymax1 = ratio_dict.get('ymax', max([np.amax(d[1][1] / base_line)
        for d in all_data]))
      ymin1 = ratio_dict.get('ymin', min([np.amin(d[1][1] / base_line)
        for d in all_data]))
      n_majors1 = ratio_dict.get('nmajors', None)
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
    label = get_label(title, pretty_label=pretty_label, object_dict=band)
    opacity = band.get('opacity', global_opacity)
    color = band.get('color', color)
    x = data_of_a_band[0][1][0]
    list_of_y_arrays = [db[1][1] for db in data_of_a_band]
    y_array = np.vstack(tuple(list_of_y_arrays))
    this_fill_between(x, np.amin(y_array, axis=0), np.amax(y_array, axis=0),
        color=color, label=label, alpha=opacity)
  for td, c in zip(line_data, colors):
    filename, d = td[0], td[1]
    label = get_label(title, filename=filename, pretty_label=pretty_label)
    linestyle = decide_or_get(linestyle_decider, 'linestyle', None, filename, title)
    if linestyle == 'banded':
      if len(d) > 2:
        plt.fill_between(d[0], d[1] - d[2], d[1] + d[2],
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
    elif linestyle is not None:
      this_plot(d[0], d[1], color=c, label=label, linestyle=linestyle)
    else:
      if marker_decider is not None:
        marker = marker_decider(filename, title)
      else:
        marker = plot_dict.get('marker', '+')
      if len(d) > 2:
        ax.errorbar(d[0], d[1], fmt=marker, yerr=d[2], color=c, label=label)
      else:
        ax.errorbar(d[0], d[1], fmt=marker, color=c, label=label)
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
  pl.setfig(ax, title=title,
            xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
            xminors=xminors, yminors=yminors,
            xlabel=xlabel,
            ylabel=ylabel, ylog=ylog, xlog=xlog,
            legend_outside=many_labels, height_shrinker=0.70,
            legend_location=legend_location, ax1=ax1, ylabel1=ylabel1,
            ymin1=ymin1, ymax1=ymax1, n_majors1=n_majors1)
  fig.savefig(os.path.join(pic_path, title + '.pdf'),
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
