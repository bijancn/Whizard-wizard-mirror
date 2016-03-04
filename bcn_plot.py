import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib._cm import cubehelix
from matplotlib.ticker import *
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
          #'#cddc39',  # lime
          '#3f51b5'   # indigo
          #'#009688',  # teal
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
      n_minors=5, n_majors=5, xticks=None, yticks=None, puff=0.05, legend_location='best',
      legend_columns=1, legend_outside=False, height_shrinker=0.80,
      legend_hide=False, legend_ordering=[]):
    # label axes and set ranges and scales
    if xlabel is not None:
      ax.set_xlabel(xlabel)
    if ylabel is not None:
      ax.set_ylabel(ylabel)
    _set_puffed_scale(puff, xmax, xmin, xlog, ax.set_xlim, ax.set_xscale)
    _set_puffed_scale(puff, ymax, ymin, ylog, ax.set_ylim, ax.set_yscale)

    # title (ensuring no double set)
    if title is not None and self.title_notset:
      plt.suptitle(title, y=0.99)
      #plt.text(0.7, 1.01, title,
         #horizontalalignment='center',
         #transform = ax.transAxes)
      self.title_notset = False

    # tight layout with extra padding
    # pad : padding between the figure edge and the edges of subplots, as a
    #       fraction of the font-size
    # h_pad, w_pad : padding (height/width) between edges of adjacent subplots.
    #                Defaults to pad_inches
    #rect : if rect is given, it is interpreted as a rectangle
    #       (left, bottom, right, top) in the normalized figure coordinate that
    #       the whole subplots area (including labels) will fit into.
    #       Default is (0, 0, 1, 1)
    #       We set top to 0.96 to have space for title
    if self.layout_notset:
      plt.tight_layout(pad=0.5, rect=[0.04, 0.00, 1, 0.96])
      self.layout_notset = False

    # major ticks
    if xticks is None:
      xticks = np.linspace(xmin, xmax, n_majors)
    ax.set_xticks(xticks)
    if yticks is None:
      yticks = np.linspace(ymin, ymax, n_majors)
    ax.set_yticks(yticks)

    # minor ticks are auto-set to n_minors if requested
    if xminors:
      minorLocator = AutoMinorLocator(n_minors)
      ax.xaxis.set_minor_locator(minorLocator)
    if yminors:
      minorLocator = AutoMinorLocator(n_minors)
      ax.yaxis.set_minor_locator(minorLocator)

    # This should allow to use scientific format of logarithmic scale with 10^X
    # above the axe.
    #formatter = ScalarFormatter(useMathText=True)
    #formatter.set_scientific(True)
    #formatter.set_powerlimits((-1,1))
    #ax.yaxis.set_major_formatter(formatter)

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
        ax.set_position([box.x0, box.y0 + box.height * (1.0-height_shrinker),
                         box.width, box.height * height_shrinker])
        # Put a legend below current axis
        ax.legend(handles, labels, loc='upper center',
            bbox_to_anchor=(0.5, -0.1),
            fancybox=False, ncol=legend_columns)
      else:
        ax.legend(handles, labels, loc=legend_location,
                  fancybox=False, ncol=legend_columns)

def check_for_all_sets(found_lines, wanted_lines, data):
  if len(found_lines) < len(wanted_lines):
    print 'Did not find all sets: But only ', len(found_lines), \
          ' out of ', len(wanted_lines)
    for l in wanted_lines:
      if not l in [lbl[0] for lbl in found_lines]:
        print l, ' not found!'
    print 'The available data is ', data
    sys.exit(1)

def set_if_not_none(plot_dict, decider, thing_to_set, default, *args):
  if decider is not None:
    return decider(args)
  else:
    return plot_dict.get(thing_to_set, default)

def plot(plot_dict, data, pic_path='./', plot_extra=None, range_decider=None,
    label_decider=None, legend_decider=None, marker_decider=None,
    linestyle_decider=None, pretty_label=None, set_extra_settings=None):
  mkdirs(pic_path)
  title = plot_dict.get('title', 'plot')
  print 'Plotting ' + title
  this_data = []
  lines = plot_dict.get('lines', [])
  for lbl in lines:
    this_data += [d for d in data if lbl in d[0]]
  many_labels = len(this_data) > 6
  check_for_all_sets(this_data, lines, data)
  size = (9,9) if many_labels else (9,7.5)
  fig = plt.figure(figsize = size)
  ax = fig.add_subplot(1,1,1)
  set_if_not = partial(set_if_not_none, plot_dict)
  if plot_extra is not None:
    ax = plot_extra(ax, title)
  if range_decider is not None:
    ymin, ymax, xmin, xmax = range_decider(this_data, title)
  else:
    ymin = min([np.amin(d[1][1]) for d in this_data])
    ymax = max([np.amax(d[1][1]) for d in this_data])
    xmin = min([np.amin(d[1][0]) for d in this_data])
    xmax = min([np.amax(d[1][0]) for d in this_data])
  if label_decider is not None:
    xlabel, ylabel = label_decider (title)
  else:
    xlabel, ylabel = (plot_dict.get('xlabel', 'x'), plot_dict.get('ylabel', 'y'))
  # TODO: (bcn 2016-03-03) check that this works
  legend_location = set_if_not (legend_decider, 'legend_location', 'best', title)
  if legend_decider is not None:
    legend_location = legend_decider (title)
  else:
    legend_location = plot_dict.get('legend_location', 'best')
  if set_extra_settings is not None:
    ax = set_extra_settings(ax, title)
  # if plot_dict.get('plot_type', 'default') == 'fill_band':
  # Use matplotlib's fill_between() call to create error bars.
  # plt.fill_between(years, mean_PlyCount - sem_PlyCount,
             # mean_PlyCount + sem_PlyCount, color="#3F5D7D")
  pl = Plotter()
  i = 0
  for td,c in zip(this_data, colors):
    l, d = td[0], td[1]
    print l
    lbl = pretty_label(l, title) if pretty_label is not None else os.path.basename(l)
    lbl = lbl.replace('_', '\_')
    if linestyle_decider is not None:
      linestyle = linestyle_decider (l, title)
    else:
      linestyle = plot_dict.get('linestyle', None)
    if linestyle is not None:
      ax.plot(d[0], d[1], color=c, label=lbl, linestyle=linestyle)
    else:
      if marker_decider is not None:
        marker = marker_decider(l, title)
      else:
        marker = plot_dict.get('marker', '+')
      if len(d) > 2:
        ax.errorbar(d[0], d[1], fmt=marker, yerr=d[2], color=c, label=lbl)
      else:
        ax.errorbar(d[0], d[1], fmt=marker, color=c, label=lbl)
    if plot_dict.get('generate_animated', False):
      i += 1
      pl.setfig(ax, title=None,
                xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
                xminors=True, yminors=True,
                xlabel=xlabel,
                ylabel=ylabel, ylog=False, xlog=False,
                legend_outside=many_labels, height_shrinker=0.70,
                legend_location=legend_location,
                legend_hide=False)
      fig.savefig(os.path.join(pic_path,  title + '-' + str(i) + '.pdf'),
                  dpi=fig.dpi)
  pl.setfig(ax, title=title,
            xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
            xminors=True, yminors=True,
            xlabel=xlabel,
            ylabel=ylabel, ylog=False, xlog=False,
            legend_outside=many_labels, height_shrinker=0.70,
            legend_location=legend_location)
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
    puffs = puff * np.log(smax-smin)
    ax_set_slim(np.exp(np.log(smin) - puffs),
                np.exp(np.log(smax) + puffs))
    ax_set_sscale('log')
  else:
    puffx = puff * (smax - smin)
    ax_set_slim(smin - puffx, smax + puffx)

def _norm(x):
  if (x>1.0):
    return 1.0
  if (x<0.0):
    return 0.0
  return x