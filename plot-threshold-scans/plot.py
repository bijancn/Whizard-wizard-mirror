from bcn_plot import *
import os.path
import matplotlib.gridspec as gridspec
pic_path = os.path.abspath('./') + '/'
colors = ['#EE3311',  # red
          '#3366FF',  # blue
          '#109618',  # green
          '#FF9900',  # orange
          '#990099',  # lilac
          '#000000']  # black

files = ['./ttbar_lo_onshell.dat', './ttbar_nlo_onshell.dat',
         './ttbar_lo_offshell.dat', './ttbar_lo_offshell_restricted.dat']
#, './christian_scan_total_lo.dat', './christian_scan_total_nlo.dat']
labels = ['LO Onshell', 'NLO Onshell', 'LO Offshell', 'LO Offshell Restricted']
#,
          #'Christian LO Offshell', 'Christian NLO Offshell']
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
data = [np.loadtxt(filename, unpack=True) for filename in files]

#x, y, yerr = np.loadtxt(f, unpack=True)

for d,c,l in zip(data, colors, labels):
  ax.plot(d[0], d[1], color=c, label=l)
  #ax.errorbar(d[0], d[1], fmt='+', yerr=d[2], color=c, label=l)

xmin = min([np.amin(d[0]) for d in data])
xmax = max([np.amax(d[0]) for d in data])
ymin = min([np.amin(d[1]) for d in data])
ymax = max([np.amax(d[1]) for d in data])
xmax = 450

pl = Plotter()
pl.setfig(ax, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
    xlabel='$\\sqrt{s}$',
    ylabel='$\\sigma$', ylog = False, xlog = False)

fig.savefig(pic_path + 'threshold-scan.pdf', dpi=fig.dpi)
