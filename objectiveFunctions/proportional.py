from typing import Any
from xmlrpc.client import MAXINT
from utils.distances import dist
from numpy import ndarray, array, concatenate

# Alternatively, Huff model
def proportional(X: 'ndarray[int]', args: dict[str, Any]):
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

def partiallyProportional(X: 'ndarray[int]', args: dict[str, Any]):
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

def getParetoOptimalLocations(i: int, J: 'list[(int, int)]', K: 'list[(int, int)]'):
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
  return array(optimalJ)

def paretoProportional(X: 'ndarray[int]', args: dict[str, Any]):
  attractedPopulation = 0
  for i in range(len(args['population'])):
    aX = 0
    aJ = 0
    minaj = MAXINT
    maxaj = 0
    J = array([(j, qj) for firm in args['competitors'] for j, qj in firm])
    paretoJ = getParetoOptimalLocations(i, J, concatenate([X, J]))
    paretoX = getParetoOptimalLocations(i, X, concatenate([X, J]))

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