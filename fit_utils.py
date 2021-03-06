# Various tools for fitting functions to our data (used by data_utils.py)
import numpy as np


def fit_line(x, y, xmin, xmax, verbose=False):
  # Needs statsmodels which can be installed by checking out the following repo:
  # git clone git://github.com/statsmodels/statsmodels.git
  import statsmodels.api as sm
  regression = sm.OLS(y, sm.add_constant(x)).fit()
  if verbose:
    print regression.summary()
  fit_x = np.linspace(xmin, xmax, 100)
  fit_y = fit_x * regression.params[1] + regression.params[0]
  return fit_x, fit_y


def fit_polynomial(x, y, xmin, xmax, degree, y_err=None, verbose=False):
  # parameters, residuals, _, _, _ = np.polyfit(x, y, degree, w=y_err, full=True)
  parameters, cov = np.polyfit(x, y, degree, w=y_err, cov=True)
  parameter_errors = np.diagonal(cov)
  if verbose:
    print 'Polynomial coefficients: '
    for i in range(degree + 1):
      print 'C[' + str(i) + ']= ' + str(parameters[degree - i]) + \
          ' +- ' + str(parameter_errors[degree - i])
  delta_x = 10
  x_work = x
  if xmin < x_work[0]:
    np.insert(x_work, xmin, 0)
  if xmax > x_work[len(x) - 1]:
    np.concatenate(x_work, xmax)
  fit_x = np.zeros(0)
  for i in range(len(x_work) - 1):
    fit_x = np.append(fit_x, np.linspace(x_work[i], x_work[i + 1], delta_x))

  fit_y = np.zeros(len(fit_x))
  for i in range(degree + 1):
    fit_y += pow(fit_x, i) * parameters[degree - i]
  return fit_x, fit_y
