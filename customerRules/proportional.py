from typing import Any
from xmlrpc.client import MAXINT
from utils.distances import dist
import numpy as np

# Alternatively, Huff model
def proportional(X: 'np.ndarray[int]', args: dict[str, Any]):
  attractedPopulation = 0
  for i in range(len(args['population'])):
    aX = 0
    aJ = 0
    minaj = MAXINT
    maxaj = 0
    for firm in args['competitors']:
      for j, qj in firm:
        aj = qj / (1 + dist(i, j))
        aJ += aj
        if aj < minaj: minaj = aj
        elif aj > maxaj: maxaj = aj
    minA = minaj + args['minAttraction'] * (maxaj - minaj)
    for x, qx in X:
      d = dist(i, x)
      ax = qx / (1 + d)
      if ax >= minA: aX += ax
    attractedPopulation += aX / (aX + aJ) * args['population'][i]
  return attractedPopulation/args['totalPopulation']*100

def partiallyProportional(X: 'np.ndarray[int]', args: dict[str, Any]):
  attractedPopulation = 0
  for i in range(len(args['population'])):
    aX = 0
    aJ = 0
    minaj = MAXINT
    maxaj = 0
    for firm in args['competitors']:
      localMaxaj = 0
      for j, qj in firm:
        aj = qj / (1 + dist(i, j))
        if aj > localMaxaj: localMaxaj = aj
        if aj < minaj: minaj = aj
        elif aj > maxaj: 
          maxaj = aj
      # only picks a single facility with maximum attraction, even if there are multiple
      aJ += localMaxaj
    minA = minaj + args['minAttraction'] * (maxaj - minaj)
    for x, qx in X:
      d = dist(i, x)
      ax = qx / (1 + d)
      if ax >= minA: aX += ax
    attractedPopulation += aX / (aX + aJ) * args['population'][i]
  return attractedPopulation/args['totalPopulation']*100

def getParetoOptimalLocations(i: int, J: 'np.ndarray[(int, int)]', K: 'np.ndarray[(int, int)]'):
  optimalJ = []
  for j, qj in J:
    isOptimal = True
    # facility j is amongst pareto optimal facilities if its there are no facilities 
    # with shorter distances and same/better qualities or same distances and better qualities 
    for k, qk in K:
      if dist(i, k) < dist(i, j) and qk >= qj or \
        dist(i, k) == dist(i, j) and qk > qj:
        isOptimal = False
        break
    if isOptimal: optimalJ.append((j, qj))
  return np.array(optimalJ)

def paretoProportional(X: 'np.ndarray[int]', args: dict[str, Any]):
  attractedPopulation = 0
  for i in range(len(args['population'])):
    aX = 0
    aJ = 0
    minaj = MAXINT
    maxaj = 0
    J = np.array([(j, qj) for firm in args['competitors'] for j, qj in firm])
    paretoJ = getParetoOptimalLocations(i, J, np.concatenate([X, J]))
    paretoX = getParetoOptimalLocations(i, X, np.concatenate([X, J]))

    # the rest is identical to the proportional model
    for j, qj in paretoJ:
      aj = qj / (1 + dist(i, j))
      aJ += aj
      if aj < minaj: minaj = aj
      elif aj > maxaj: maxaj = aj
    minA = minaj + args['minAttraction'] * (maxaj - minaj)
    for x, qx in paretoX:
      d = dist(i, x)
      ax = qx / (1 + d)
      if ax >= minA: aX += ax
    attractedPopulation += aX / (aX + aJ) * args['population'][i]
  return attractedPopulation/args['totalPopulation']*100