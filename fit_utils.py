# Various tools for fitting functions to our data
# Needs statsmodels which can be installed by checking out the following repo:
# git clone git://github.com/statsmodels/statsmodels.git
import numpy as np


def fit_line(x, y, verbose=False):
  import statsmodels.api as sm
  regression = sm.OLS(y, sm.add_constant(x)).fit()
  if verbose:
    print regression.summary()
  fit_x = np.linspace(min(x), max(x), 100)
  fit_y = fit_x * regression.params[1] + regression.params[0]
  return fit_x, fit_y
