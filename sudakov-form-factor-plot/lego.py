from mpl_toolkits.mplot3d import Axes3D
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import sys

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# X, Y, Z = axes3d.get_test_data(0.05)
file_name = '/home/bijancn/BitPocket/extra_nlo_tt_powheg_sudakov_1000000_powheg_grids.dat'
scan_points = 200

mpl.rcParams.update({'font.size': 10})

def index(points, ix, iy, iz):
  return ix + iy * points[0] + iz * points[0] * points[1]

def grid_value(grid, points, ix, iy, iz):
  return grid[index(points, ix, iy, iz)]

def grid_func(X, Y, XX, alr):
  Z = []
  for x in Xscan:
    for ix in range(points[0]):
      if (x < (ix+1) * width[0]):
        break
    for y in Yscan:
      for iy in range(points[1]):
        if (y < (iy+1) * width[1]):
          break
      Z.append(grid_value(grid, points, ix, iy, alr))
  Z = np.array(Z)
  Z = Z.reshape(XX.shape)
  return Z

with open(file_name) as f:
  ndim = int(f.next())
  points = map(int, f.next().split())
  grid = map(float, f.next().split())
  width = []
  for dim in range(ndim):
    width.append(1.0 / points[dim])

  Xscan = np.linspace(0.0, 1.0, scan_points)
  Yscan = np.linspace(0.0, 1.0, scan_points)
  X, Y = np.meshgrid(Xscan, Yscan)
  Z1 = grid_func (Xscan, Yscan, X, 0)
  Z2 = grid_func (Xscan, Yscan, X, 1)
  print np.max(Z1)
  print np.min(Z1)
  print np.max(Z2)
  print np.min(Z2)
  ax.plot_surface(X, Y, Z1, cmap=mpl.cm.hot, alpha=0.5)
  ax.plot_surface(X, Y, Z2, cmap=mpl.cm.hot, alpha=0.5)
  ax.set_xlabel('$\\xi$')
  ax.set_ylabel('$y$')
  ax.dist = 25
  ax.view_init(elev=20, azim=45)

  plt.show()

# zs = np.array([fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
# Z = zs.reshape(X.shape)
  # zi = griddata(Xscan, Yscan, Z, Xscan, Yscan, interp='linear')
  # xx, yy = np.meshgrid(X, Y)
  # ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
