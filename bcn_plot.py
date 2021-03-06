# main functions for plotting. Used by plot-data.py

import sys
import os
import math
import numpy as np
from matplotlib._cm import cubehelix
from matplotlib.ticker import AutoMinorLocator
from matplotlib import rc_file
from matplotlib import gridspec
import matplotlib.pyplot as plt
import data_utils
from data_utils import get_name
from functools import partial
from utils import mkdirs
try:
  import mpld3
except:
  mpld3 = None
rc = os.path.join(os.getcwd(), '../matplotlibrc')
print 'Loading rc : ', rc
rc_file(rc)

colors = ['#EE3311',  # red
          '#3366FF',  # blue
          '#109618',  # green
          '#FF9900',  # orange
          '#80deea',  # cyan
          '#ab47bc',  # purple
          '#000000',  # black
          '#f06292',  # pink
          '#CDDC39',  # lime
          '#303F9F',  # indigo
          '#795548',  # brown
          '#FFEB3B',  # yellow
          '#FF7043',  # deeporange
          '#009688',  # teal
          '#607D8B',  # bluegray
          '#EF9A9A'   # lightred
          ]

color_names = [
    "red",
    "blue",
    "green",
    "orange",
    "cyan",
    "purple",
    "black",
    "pink",
    "lime",
    "indigo",
    "brown",
    "yellow",
    "deeporange",
    "teal",
    "bluegray",
    "lightred"
]

color_dict = dict(zip(color_names, colors))

N_YMINORS_DEFAULT = 4
N_XMINORS_DEFAULT = 4
N_YMAJORS_DEFAULT = 6
N_XMAJORS_DEFAULT = 6


def use_defined_colors(col_string):
  return color_dict.get(col_string, col_string)


def set_labels(axes, xlabel, ylabels):
  if xlabel is not None:
    combined_axes = [ax for ax in axes if 'Subplot' in str(type(ax))]
    combined_axes[-1].set_xlabel(xlabel)
    independent_axes = [ax for ax in axes if 'Subplot' not in str(type(ax))]
    [ia.set_xlabel(xlabel) for ia in independent_axes]
  for ax, ylabel in zip(axes, ylabels):
    if ylabel is not None:
      ax.set_ylabel(ylabel)


def auto_tick_labeling(ticks):
  max_tick = max(abs(ticks))
  if max_tick < 10:
    tick_str = "{:.2f}"
  elif max_tick < 100:
    tick_str = "{:.1f}"
  elif max_tick < 10000:
    tick_str = "{:.0f}"
  else:
    tick_str = "{:.2e}"
  return ["$" + tick_str.format(tick) + "$" for tick in ticks]


def set_x_ticks(xticks, combined_axes, xlog, xmin, xmax, xmajors):
  if xticks is None:
    if xlog:
      if xmin <= 0:
        raise Exception("You should set xmin > 0 in a log plot")
      else:
        xticks = np.logspace(math.log10(xmin), math.log10(xmax), num=xmajors)
    else:
      xticks = np.linspace(xmin, xmax, xmajors)
    combined_axes[-1].set_xticklabels(auto_tick_labeling(xticks))
  else:
    combined_axes[-1].set_xticklabels(["$" + str(xt) + "$" for xt in xticks])
  combined_axes[-1].set_xticks(xticks)


def set_y_ticks(ytickss, axes, ylogs, ymins, ymaxs, ymajorss):
  for ymax, ymin, ymajors, yticks, ylog, ax in zip(ymaxs, ymins, ymajorss,
      ytickss, ylogs, axes):
    if yticks is None:
      if ylog:
        if ymin <= 0:
          raise Exception("You should set ymin > 0 in a log plot")
        else:
          yticks = np.logspace(math.log10(ymin), math.log10(ymax), num=ymajors)
      else:
        yticks = np.linspace(ymin, ymax, ymajors)
      ax.set_yticklabels(auto_tick_labeling(yticks))
    else:
      ax.set_yticklabels(["$" + str(yt) + "$" for yt in yticks])
    ax.set_yticks(yticks)


def set_major_ticks(axes, xticks, ytickss, xmin, xmax, xmajors, ymins, ymaxs,
          ymajorss, xlog, ylogs):
  if type(axes) == list:
    combined_axes = [ax for ax in axes if 'Subplot' in str(type(ax))]
  else:
    combined_axes = [axes]
    axes = [axes]
  set_x_ticks(xticks, combined_axes, xlog, xmin, xmax, xmajors)
  for ax in combined_axes[:-1]:
    plt.setp(ax.get_xticklabels(), visible=False)
  set_y_ticks(ytickss, axes, ylogs, ymins, ymaxs, ymajorss)


def set_minor_ticks(axes, xminors, yminorss, xlog, ylogs):
  for ax, yminors, ylog in zip(axes, yminorss, ylogs):
    ax.minorticks_off()
    if xminors is None:
      xminors = N_XMINORS_DEFAULT
    if xlog:
      ax.set_xscale('log')
    else:
      minorLocator = AutoMinorLocator(xminors + 1)
      ax.xaxis.set_minor_locator(minorLocator)
    if yminors is None:
      yminors = N_YMINORS_DEFAULT
    if ylog:
      ax.set_yscale('log')
    else:
      minorLocator = AutoMinorLocator(yminors + 1)
      ax.yaxis.set_minor_locator(minorLocator)


def set_legend(fig, axes, legend_ordering, legend_outside, height_shrinker,
    legend_columns, legend_location):
  handles, labels = axes[0].get_legend_handles_labels()
  if len(legend_ordering) == len(handles):
    # reorder if sequence of appropriate size is given
    handles = map(handles.__getitem__, legend_ordering)
    labels = map(labels.__getitem__, legend_ordering)
  if legend_outside == 'vertical':
    # Shrink current axis's height by (1.0-height_shrinker) on the bottom
    reduced_amount = 0.0
    for ax in axes:
      box = ax.get_position()
      ax.set_position([box.x0, box.y0 + reduced_amount + box.height * (1.0 -
        height_shrinker), box.width, box.height * height_shrinker])
      reduced_amount = box.height * (1.0 - height_shrinker)
    fig.legend(handles, labels, loc='lower center',
        bbox_to_anchor=(0.5, 0.0),
        fancybox=False, ncol=legend_columns)
  elif legend_outside == 'horizontal':
    #  reduced_amount = 0.0
    #  for ax in axes:
    #    box = ax.get_position()
    #    ax.set_position([box.x0 + reduced_amount + box.width * (1.0 -
    #      height_shrinker), box.y0, box.width * height_shrinker, box.height])
    #    reduced_amount = box.width * (1.0 - height_shrinker)
    ax = axes[0]
    ax.legend(handles, labels, loc='upper left',
        bbox_to_anchor=(1.02, 1), borderaxespad=0,
        fancybox=False, ncol=legend_columns)
    plt.draw()         # to know size of legend
    padLeft = ax.get_position().x0 * fig.get_size_inches()[0]
    padBottom = ax.get_position().y0 * fig.get_size_inches()[1]
    padTop = (1 - ax.get_position().y0 - ax.get_position().height) * \
        fig.get_size_inches()[1]
    padRight = (1 - ax.get_position().x0 - ax.get_position().width) * \
        fig.get_size_inches()[0]
    dpi = fig.get_dpi()
    padLegend = ax.get_legend().get_frame().get_width() / dpi
    widthAx = 9
    heightAx = 9
    widthTot = widthAx + padLeft + padRight + padLegend
    heightTot = heightAx + padTop + padBottom
    # set figure size and ax position
    fig.set_size_inches(widthTot, heightTot)
    ax.set_position([padLeft / widthTot, padBottom / heightTot,
                     widthAx / widthTot, heightAx / heightTot])
    plt.draw()

  else:
    #  TODO: (bcn 2016-08-17) in general one could imagine to give the ax to
    #  draw the legend on
    axes[0].legend(handles, labels, loc=legend_location,
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
      plt.tight_layout(pad=0.5, h_pad=2.0, w_pad=2.0, rect=[0.04, 0.00, 1, 0.96])
      plt.subplots_adjust(hspace=0.05)
      self.layout_notset = False

  def setfig(self, fig, axes, xmin, xmax, ymins, ymaxs, xlabel, ylabels,
      title=None, xlog=False, ylogs=[],
      xmajors=N_XMAJORS_DEFAULT, ymajorss=[],
      xminors=0, yminorss=[],
      xticks=None, ytickss=[], puff=0.05,
      legend_location='best',
      legend_columns=1, legend_outside="Nope", height_shrinker=0.80,
      legend_hide=False, legend_ordering=[]):
    set_labels(axes, xlabel, ylabels)
    for ax in axes:
      _set_puffed_scale(puff, xmax, xmin, xlog, ax.set_xlim, ax.set_xscale)
    for ymax, ymin, ylog, ax in zip(ymaxs, ymins, ylogs, axes):
      _set_puffed_scale(puff, ymax, ymin, ylog, ax.set_ylim, ax.set_yscale)
    if title is not None and self.title_notset:
      plt.suptitle(title, y=0.99, x=0.55)
      self.title_notset = False
    self.set_layout()
    set_minor_ticks(axes, xminors, yminorss, xlog, ylogs)
    set_major_ticks(axes, xticks, ytickss, xmin, xmax, xmajors, ymins, ymaxs,
          ymajorss, xlog, ylogs)
    if not legend_hide:
      set_legend(fig, axes, legend_ordering, legend_outside, height_shrinker,
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


def handle_base_line_exceptions(base_lines, axes):
  if type(base_lines) != list:
    base_lines = [base_lines] * len(axes[1:])
  if len(axes[1:]) != len(base_lines):
    print 'Inconsistent number of ratios and base_lines!'
    print 'len(axes[1:]) = ', len(axes[1:])
    print 'len(base_lines) = ', len(base_lines)
  return base_lines


def combined_plot(axes, base_lines, x, y, *args, **kwargs):
  axes[0].plot(x, y, *args, **kwargs)
  base_lines = handle_base_line_exceptions(base_lines, axes)
  for ax, base_line in zip(axes[1:], base_lines):
    if base_line is not None:
      comb = data_utils.normalize(base_line, x, y)
      ax.plot(comb[0], comb[1], *args, **kwargs)


def combined_errorbar(axes, base_lines, x, y, yerr=None, **kwargs):
  axes[0].errorbar(x, y, yerr=yerr, **kwargs)
  base_lines = handle_base_line_exceptions(base_lines, axes)
  for ax, base_line in zip(axes[1:], base_lines):
    comb = data_utils.normalize(base_line, x, y, yerr=yerr)
    if len(comb[0]) != len(comb[1]):
      raise Exception("normalize gave incoherent data: len(x) != len(y): " +
          str(len(comb[0])) + " != " + str(len(comb[1])))
    ax.errorbar(comb[0], comb[1], yerr=comb[2], **kwargs)


def combined_fill_between(axes, base_lines, x, ymin, ymax, *args, **kwargs):
  axes[0].fill_between(x, ymin, ymax, *args, **kwargs)
  base_lines = handle_base_line_exceptions(base_lines, axes)
  for ax, base_line in zip(axes[1:], base_lines):
    if base_line is not None:
      comb = data_utils.normalize(base_line, x, ymin, yerr=ymax)
      ax.fill_between(comb[0], comb[1], comb[2], *args, **kwargs)


#  TODO: (bcn 2016-08-17) is this art or can it go?
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


def sanity_check(data):
  for dat in data:
    if not (type(dat[0]) is str or type(dat[0]) is unicode):
      print 'This is not an identifier_string:', dat[0], type(dat[0])
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


def append_from_ratio_dict(ratio_dict, attribute, lst, default_val=None):
  if ratio_dict is not None:
    if type(ratio_dict) != list:
      ratio_dict = [ratio_dict]
    for rd in ratio_dict:
      lst.append(rd.get(attribute, default_val))
  return lst


def setup_fig_kwargs(line_data, band_data, many_labels, plot_dict, ratio_dict):
  fig_kwargs = setup_ranges(line_data, band_data, plot_dict, ratio_dict)
  fig_kwargs.update(setup_labels(plot_dict, ratio_dict))
  fig_kwargs.update(setup_log_scale(plot_dict, ratio_dict))
  fig_kwargs.update(setup_ticks(plot_dict, ratio_dict))
  fig_kwargs.update(setup_majors(plot_dict, ratio_dict))
  fig_kwargs.update(setup_minors(plot_dict, ratio_dict))
  fig_kwargs.update(setup_extra_kwargs(plot_dict, many_labels))
  return fig_kwargs


def setup_figure(plot_dict, ratio_dict, many_labels):
  try:
    size = (plot_dict['xpagelength'], plot_dict['ypagelength'])
  except KeyError:
    size = (9, 9) if many_labels else (9, 7.5)
  return plt.figure(figsize=size)


def setup_ranges(line_data, band_data, plot_dict, ratio_dict):
  try:
    flattened_band_data = reduce(lambda x, y: x + y, band_data)
  except TypeError:
    flattened_band_data = []
  all_data = line_data + flattened_band_data
  xmin = plot_dict.get('xmin', min([np.amin(d[1][0]) for d in all_data]))
  xmax = plot_dict.get('xmax', min([np.amax(d[1][0]) for d in all_data]))
  ymins = [plot_dict.get('ymin', min([np.amin(d[1][1]) for d in all_data]))]
  ymaxs = [plot_dict.get('ymax', max([np.amax(d[1][1]) for d in all_data]))]
  ymins = append_from_ratio_dict(ratio_dict, 'ymin', ymins)
  ymaxs = append_from_ratio_dict(ratio_dict, 'ymax', ymaxs)
  return {'xmin': xmin, 'xmax': xmax, 'ymins': ymins, 'ymaxs': ymaxs}


def setup_labels(plot_dict, ratio_dict):
  xlabel = plot_dict.get('xlabel', 'x')
  ylabels = [plot_dict.get('ylabel', 'y')]
  ylabels = append_from_ratio_dict(ratio_dict, 'ylabel', ylabels)
  return {'xlabel': xlabel, 'ylabels': ylabels}


def setup_log_scale(plot_dict, ratio_dict):
  xlog = plot_dict.get('xlog', False)
  ylogs = [plot_dict.get('ylog', False)]
  ylogs = append_from_ratio_dict(ratio_dict, 'ylog', ylogs)
  return {'xlog': xlog, 'ylogs': ylogs}


def setup_ticks(plot_dict, ratio_dict):
  xticks = plot_dict.get('xticks', None)
  ytickss = [plot_dict.get('yticks', None)]
  ytickss = append_from_ratio_dict(ratio_dict, 'yticks', ytickss)
  return {'xticks': xticks, 'ytickss': ytickss}


def setup_majors(plot_dict, ratio_dict):
  xmajors = plot_dict.get('xmajors', N_XMAJORS_DEFAULT)
  ymajorss = [plot_dict.get('ymajors', N_YMAJORS_DEFAULT)]
  ymajorss = append_from_ratio_dict(ratio_dict, 'ymajors', ymajorss,
                                    N_YMAJORS_DEFAULT)
  return {'xmajors': xmajors, 'ymajorss': ymajorss}


def setup_minors(plot_dict, ratio_dict):
  xminors = plot_dict.get('xminors', None)
  yminorss = [plot_dict.get('yminors', None)]
  yminorss = append_from_ratio_dict(ratio_dict, 'yminors', yminorss)
  return {'xminors': xminors, 'yminorss': yminorss}


def setup_extra_kwargs(plot_dict, many_labels):
  kwargs = {}
  kwargs['height_shrinker'] = plot_dict.get('legend_height_shrinker', 0.7)
  legend_outside = "vertical" if many_labels else "Nope"
  kwargs['legend_outside'] = plot_dict.get('legend_outside', legend_outside)
  kwargs['legend_location'] = plot_dict.get('legend_location', 'best')
  kwargs['legend_ordering'] = plot_dict.get('legend_ordering', [])
  return kwargs


def plot_band(data_of_a_band, band, color, title, global_opacity, pretty_label,
  this_fill_between):
  label = get_label(band, title, pretty_label=pretty_label)
  opacity = band.get('opacity', global_opacity)
  color = use_defined_colors(band.get('color', color))
  list_of_y_arrays = [db[1][1] for db in data_of_a_band]
  list_of_x_arrays = [db[1][0] for db in data_of_a_band]
  combined_x, list_of_y_arrays = data_utils.remove_uncommon(list_of_x_arrays,
      list_of_y_arrays)
  y_array = np.vstack(tuple(list_of_y_arrays))
  smallest = np.amin(y_array, axis=0)
  largest = np.amax(y_array, axis=0)
  if band.get('symmetrize', False):
    central = y_array[0]
    tmp = np.array(central + (central - smallest))
    new_largest = np.amax(np.vstack((largest, tmp)), axis=0)
    tmp = np.array(central - (largest - central))
    new_smallest = np.amin(np.vstack((smallest, tmp)), axis=0)
    largest = new_largest
    smallest = new_smallest
  this_fill_between(combined_x, smallest, largest,
      color=color, label=label, alpha=opacity)


def setup_kwargs(line, title, pretty_label, filename, color, global_opacity):
  label = get_label(line, title, pretty_label=pretty_label, filename=filename)
  col = use_defined_colors(line.get('color', color))
  if line.get('hide_label', False):
    label = None
  kwargs = {
      'label': label,
      'color': col,
      'alpha': global_opacity
  }
  return kwargs


def plot_line(ldata, line, color, title, pretty_label, linestyle_decider,
    marker_decider, this_errorbar, this_plot, this_fill_between, ax,
    global_opacity, plotter):
  if line.get('hide_line', False):
    return
  filename, d = ldata[0], ldata[1]
  kwargs = setup_kwargs(line, title, pretty_label, filename, color, global_opacity)
  linestyle = decide_if_not_none(line, linestyle_decider, 'linestyle', 'solid',
      filename, title)
  if linestyle == 'banded':
    if len(d) > 2:
      this_fill_between(d[0], d[1] - d[2], d[1] + d[2], **kwargs)
    else:
      raise Exception("You have to supply errors for banded linestyle")
  elif linestyle == 'scatter':
    # TODO: (bcn 2016-03-31) hacking in a ratio for now #notproud
    #  kwargs['marker'] = "+"
    ax.scatter(d[0], d[1] / d[2], **kwargs)
  elif linestyle == 'histogram':
    # TODO: (bcn 2016-03-31) hacking in a ratio for now #notproud
    nbins = 10
    n, _ = np.histogram(d[0], bins=nbins)
    sy, _ = np.histogram(d[0], bins=nbins, weights=d[1] / d[2])
    sy2, _ = np.histogram(d[0], bins=nbins, weights=d[1] / d[2] * d[1] / d[2])
    mean = sy / n
    std = np.sqrt(sy2 / n - mean * mean)
    kwargs['ecolor'] = kwargs['color']
    kwargs['yerr'] = std
    kwargs['fmt'] = "none"
    plt.errorbar((_[1:] + _[:-1]) / 2, mean, **kwargs)
    plt.hlines(mean, _[:-1], _[1:], **kwargs)
  elif linestyle is not None and linestyle != "None":
    linewidth = line.get('linewidth', 2.0)
    kwargs['linestyle'] = linestyle
    kwargs['linewidth'] = linewidth
    this_plot(d[0], d[1], **kwargs)
  else:
    kwargs['fmt'] = decide_if_not_none(line, marker_decider, 'marker', '+')
    if len(d) > 2:
      kwargs['yerr'] = d[2]
      this_errorbar(d[0], d[1], **kwargs)
    else:
      this_errorbar(d[0], d[1], **kwargs)


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
  print 'Writing to output:', out_file.replace('.pdf', '')
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
  bands = plot_dict.get('bands', [])
  band_data = data_utils.get_associated_plot_data(data, bands)
  fits = plot_dict.get('fits', [])
  fit_data = data_utils.get_associated_plot_data(data, fits, suffix='_fit')
  n_objects = len(line_data) + len(band_data) + len(fit_data)
  many_labels = n_objects > 6
  check_for_all_sets(line_data, lines)
  # check_for_all_sets(band_data, band_lst)
  if n_objects == 0:
    print 'You selected no lines or bands. Not building: ' + title
    valid = False
  return valid, line_data, band_data, fit_data, many_labels, lines, bands, fits


def use_local_or_global_base_line(ratio_dict, band_or_line, data, this_errorbar,
    this_errorbar_func, this_plot, this_plot_func, this_fill_between,
    this_fill_between_func, global_base_line):
  if ratio_dict is not None:
    base_line = band_or_line.get('base_line', None)
    if base_line is not None:
      if type(base_line) != list:
        base_line = [base_line]
      this_base_lines = []
      for bl in base_line:
        if bl.get('hide_line', False):
          this_base_lines.append(None)
        else:
          this_base_item = [d for d in data
            if get_name(bl) == d[0].replace('.dat', '')]
          if len(this_base_item) == 0:
            raise Exception('Did not find ' + str(bl) + ' ! Maybe you made a typo?')
          this_base_lines.append(this_base_item[0][1])
      this_errorbar = partial(this_errorbar_func, this_base_lines)
      this_plot = partial(this_plot_func, this_base_lines)
      this_fill_between = partial(this_fill_between_func, this_base_lines)
    else:
      this_errorbar = partial(this_errorbar_func, global_base_line)
      this_plot = partial(this_plot_func, global_base_line)
      this_fill_between = partial(this_fill_between_func, global_base_line)
  return this_errorbar, this_plot, this_fill_between


#  TODO: (bcn 2016-08-16) could this be done better with `update`?
def try_update(new_dict, reference_dict, key):
  try:
    new_dict[key] = reference_dict[key]
  except KeyError:
    pass
  return new_dict


def plot_extra_lines_and_texts(ax, plot_dict, global_opacity):
  extra_lines = plot_dict.get('extra_lines', [])
  extra_texts = plot_dict.get('extra_texts', [])
  for extra in extra_lines + extra_texts:
    extype = extra.get('type', None)
    extext = extra.get('text', None)
    kwargs = {}
    kwargs['alpha'] = extra.get('opacity', global_opacity)
    kwargs['color'] = use_defined_colors(extra.get('color', 'black'))
    if extype == "vertical":
      kwargs['linestyle'] = extra.get('linestyle', 'solid')
      ax.axvline(extra['value'], **kwargs)
    elif extype == "horizontal":
      kwargs['linestyle'] = extra.get('linestyle', 'solid')
      ax.axhline(extra['value'], **kwargs)
    elif extext is not None:
      kwargs = try_update(kwargs, extra, 'fontsize')
      kwargs = try_update(kwargs, extra, 'verticalalignment')
      kwargs = try_update(kwargs, extra, 'horizontalalignment')
      ax.text(extra['x'], extra['y'], extext, **kwargs)
    else:
      print 'Cannot draw this extra object:', extra


def prepare_plot_objects(ratio_dict, plot_dict, fig):
  if ratio_dict is not None:
    if type(ratio_dict) != list:
      ratio_dict = [ratio_dict]
    insets = [rd for rd in ratio_dict if rd.get('inset', None) is not None]
    combined_ratio_dict = [rd for rd in ratio_dict if rd.get('inset', None) is None]
    number_of_axes = len(combined_ratio_dict) + 1
    #  TODO: (bcn 2016-08-17) could be customizable
    height_ratios = [number_of_axes]
    for rd in combined_ratio_dict:
      height_ratios.append(1)
    gs = gridspec.GridSpec(number_of_axes, 1, height_ratios=height_ratios)
    ax = fig.add_subplot(gs[0])
    axes = [ax]
    for i in range(len(combined_ratio_dict)):
      axes.append(fig.add_subplot(gs[i + 1], sharex=ax))
    ins_axes = []
    for ins in insets:
      ax = plt.axes(ins['inset'])
      ins_axes.append(ax)
      axes.append(ax)
    this_errorbar = None
    this_errorbar_func = partial(combined_errorbar, axes)
    this_plot = None
    this_plot_func = partial(combined_plot, axes)
    this_fill_between = None
    this_fill_between_func = partial(combined_fill_between, axes)
    dicts = [plot_dict] + ratio_dict
  else:
    ax = fig.add_subplot(1, 1, 1)
    this_plot = ax.plot
    this_plot_func = None
    this_errorbar = ax.errorbar
    this_errorbar_func = None
    this_fill_between = ax.fill_between
    this_fill_between_func = None
    axes = [ax]
    dicts = [plot_dict]
    insets = ins_axes = []
  return ax, this_plot, this_plot_func, this_errorbar, this_errorbar_func, \
      this_fill_between, this_fill_between_func, axes, dicts, insets, ins_axes


def plot(plot_dict, data, pic_path='./',
    legend_decider=None, marker_decider=None,
    linestyle_decider=None, pretty_label=None):
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
  ratio_dict = plot_dict.get('ratio', None)
  fig = setup_figure(plot_dict, ratio_dict, many_labels)
  global_opacity = plot_dict.get('opacity', 0.3)
  ax, this_plot, this_plot_func, this_errorbar, this_errorbar_func, \
      this_fill_between, this_fill_between_func, axes, dicts, insets, ins_axes = \
      prepare_plot_objects(ratio_dict, plot_dict, fig)
  global_base_line = line_data[0][1]
  for axx, dictt in zip(axes, dicts):
    plot_extra_lines_and_texts(axx, dictt, global_opacity)
  fig_kwargs = setup_fig_kwargs(line_data, band_data, many_labels, plot_dict,
      ratio_dict)
  plotter = Plotter()
  i = 0
  for data_of_a_band, band, color in zip(band_data, bands, colors):
    this_errorbar, this_plot, this_fill_between = \
        use_local_or_global_base_line(ratio_dict, band, data, this_errorbar,
            this_errorbar_func, this_plot, this_plot_func, this_fill_between,
            this_fill_between_func, global_base_line)
    plot_band(data_of_a_band, band, color, title, global_opacity, pretty_label,
        this_fill_between)
  for ldata, line, color in zip(line_data + fit_data, lines + fits,
                                colors + colors + colors + colors):
    i += 1
    if ratio_dict is not None:
      this_errorbar, this_plot, this_fill_between = \
          use_local_or_global_base_line(ratio_dict, line, data, this_errorbar,
              this_errorbar_func, this_plot, this_plot_func, this_fill_between,
              this_fill_between_func, global_base_line)
    plot_line(ldata, line, color, title, pretty_label, linestyle_decider,
      marker_decider, this_errorbar, this_plot, this_fill_between, ax,
      global_opacity, plotter)
    if plot_dict.get('generate_animated', False):
      plotter.setfig(fig, axes, title=None, legend_hide=False, **fig_kwargs)
      fig.savefig(os.path.join(pic_path, title + '-' + str(i) + '.pdf'),
                  dpi=fig.dpi)
  plotter.setfig(fig, axes, title=title, **fig_kwargs)
  for ins, ax in zip(insets, ins_axes):
    _set_puffed_scale(0.05, ins['xmax'], ins['xmin'], ins['xlog'],
        ax.set_xlim, ax.set_xscale)
    set_major_ticks(ax, None, [], ins['xmin'], ins['xmax'], ins['xmajors'],
        [], [], [], ins['xlog'], [])
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
