import cmath


def switch_off(v1, v2, v):
  vm = (v1 + v2) / 2.0
  vw = v2 - v1
  if (v < v1):
    return 1.0
  if (v < vm):
    return 1.0 - 2 * (v - v1)**2 / (vw**2)
  if (v < v2):
    return 2 * (v - v2)**2 / (vw**2)
  if (v >= v2):
    return 0.0


def abs_v_of_sqrts(sqrts):
  Gamma = 1.4
  m = 172.0
  return abs(cmath.sqrt(complex(sqrts - 2 * m, Gamma) / m))


def real_v_of_sqrts(sqrts):
  Gamma = 1.4
  m = 172.0
  return cmath.sqrt(complex(sqrts - 2 * m, Gamma) / m).real


def imag_v_of_sqrts(sqrts):
  Gamma = 1.4
  m = 172.0
  return cmath.sqrt(complex(sqrts - 2 * m, Gamma) / m).imag
