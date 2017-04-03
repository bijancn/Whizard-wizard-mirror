import cmath
import math


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


def linearswitch_off(v1, v2, v):
  if (v < v1):
    return 1.0
  if (v < v2):
    return 1.0 - 1.0 / (v2 - v1) * (v - v1)
  if (v >= v2):
    return 0.0


def fermiswitch_off(v1, v2, v):
  vm = (v1 + v2) / 2.0
  vw = v2 - v1
  if (v < v1):
    return 1.0
  if (v < v2):
    return 1.0 / (1.0 + math.exp((v - vm) / (vw / 20.0)))
  if (v >= v2):
    return 0.0


def smoothstep(v1, v2, v):
    x = clamp((v - v1) / (v2 - v1), 0.0, 1.0)
    return 1 - x * x * (3 - 2 * x)


def clamp(x, xmin, xmax):
  if (x < xmin):
      x = xmin
  elif (x > xmax):
      x = xmax
  return x


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
