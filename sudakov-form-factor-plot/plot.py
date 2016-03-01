from bcn_plot import *
import os.path
import matplotlib.gridspec as gridspec
pic_path = os.path.abspath('./') + '/'
colors = ['#EE3311',  # red
          '#3366FF',  # blue
          '#109618',  # green
          '#FF9900',  # orange
          '#990099']  # lilac

binning, sudakov_p, sudakov_0, sudakov_m, gen_sudakov, err_gen_sudakov = \
                                    np.loadtxt('/home/bijancn/BitPocket/ttbar_sudakov.dat', unpack=True)
x = np.sqrt(binning)

fig = plt.figure()
gs = gridspec.GridSpec(4, 1)
ax1 = fig.add_subplot(gs[0:3, :])
ax2 = fig.add_subplot(gs[3, :], sharex=ax1)
ax1.label_outer()

ax1.errorbar(x, gen_sudakov, color=colors[1], fmt='.',
    label='$1-\\text{Generated emissions above $p_T$}$', yerr=err_gen_sudakov)
ax1.errorbar(x, sudakov_0, yerr=[sudakov_m-sudakov_0, sudakov_0-sudakov_p],
    color=colors[0], label='MC integration', fmt='x')
ax2.errorbar(x, gen_sudakov/sudakov_0, color=colors[1])
ax2.errorbar(x, sudakov_0/sudakov_0, yerr=[sudakov_m-sudakov_0, sudakov_0-sudakov_p],
    color=colors[0], label='MC integration')

pl = Plotter()
pl.setfig(ax1, xmin=x.min(), xmax=x.max(), ymin=0.0001, ymax=1.01,
    xlabel=None,
    ylabel='$\\Delta(p_T)$', ylog = True, xlog = True)

pl.setfig(ax2, xmin=x.min(), xmax=x.max(), ymin=0.90, ymax=4.70,
    xlabel='$p_T[\\text{GeV}]$',
    ylabel='Ratio', ylog = True, xlog = True, legend_hide = True)

#ax.text(5,4000, r'\noindent $q\bar{q}\to4g$ \\ \\ $\tau=0.05$')
fig.savefig(pic_path + 'sudakov-comparison.pdf', dpi=fig.dpi)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xx = x / x.max()
ax.plot(xx, gen_sudakov, color=colors[1])
pl.setfig(ax, xmin=xx.min(), xmax=xx.max(), ymin=0.01, ymax=1.01,
    xlabel='$p_T[\\text{GeV}]\;/\;\sqrt{s}$',
    ylabel='$\\Delta(p_T)$', ylog = False, xlog = True, legend_hide = True)
fig.savefig(pic_path + 'sudakov-solo.pdf', dpi=fig.dpi)
