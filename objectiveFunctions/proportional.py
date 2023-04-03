from typing import Any
from xmlrpc.client import MAXINT
from utils.distances import dist
from numpy import ndarray
from random import uniform

def rand(start, end): return round(uniform(start, end))
# (customer behavior)
# Pareto-huff
#   pareto optimality
# Partially proportional

# Capacitated Facility Location Problem for an entering firm (CFLP/EF)
# (problem model) constraints: minimal market share - do all new stores collect the minimum market share

# Huff model
def proportional(potentialFacilities: 'ndarray[int]', capturedObjects: list[int], args: dict[str, Any]):
  if len(capturedObjects) == 0: return 0
  attractedPopulation = 0
  for i in capturedObjects:
    aX = 0
    aJ = 0
    for x, qx in potentialFacilities:
      aX += qx / (1 + dist(i, x, args['distance']))
    for compertitorBrand in args['competitors']:
      for j, qj in compertitorBrand:
        aJ += qj / (1 + dist(i, j, args['distance']))
    attractedPopulation += aX / (aX + aJ) * args['population'][i]
  return attractedPopulation/args['totalPopulation']*100

def partiallyProportional(potentialFacilities: 'ndarray[int]', capturedObjects: list[int], args: dict[str, Any]):
  if len(capturedObjects) == 0: return 0
  attractedPopulation = 0
  for i in capturedObjects:
    aX = 0
    aJ = 0
    minaj = MAXINT
    maxaj = 0
    for compertitorBrand in args['competitors']:
      for j, qj in compertitorBrand:
        aj = qj / (1 + dist(i, j, args['distance']))
        aJ += aj
        if aj < minaj: minaj = aj
        elif aj > maxaj: maxaj = aj
    minA = minaj + args['minAttrMult'] * (maxaj - minaj)
    for x, qx in potentialFacilities:
      d = dist(i, x, args['distance'])
      ax = qx / (1 + d)
      if ax >= minA: aX += ax
    attractedPopulation += aX / (aX + aJ) * args['population'][i]
  return attractedPopulation/args['totalPopulation']*100