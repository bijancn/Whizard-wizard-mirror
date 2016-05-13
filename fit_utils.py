# Various tools for fitting functions to our data
# Needs statsmodels which can be installed by checking out the following repo:
# git clone git://github.com/statsmodels/statsmodels.git
import numpy as np


def fit_line(x, y, xmin, xmax, verbose=False):
  import statsmodels.api as sm
  regression = sm.OLS(y, sm.add_constant(x)).fit()
  if verbose:
    print regression.summary()
  fit_x = np.linspace(xmin, xmax, 100)
  fit_y = fit_x * regression.params[1] + regression.params[0]
  return fit_x, fit_y


def fit_polynomial(x, y, xmin, xmax, degree, verbose=False):
  parameters, parameter_errors, _, _, _ = np.polyfit(x, y, degree, full=True)
  fit_x = np.linspace(xmin, xmax, 100)
  fit_y = np.zeros(100)
  for i in range(degree + 1):
    fit_y += pow(fit_x, i) * parameters[degree - i]
  return fit_x, fit_y
