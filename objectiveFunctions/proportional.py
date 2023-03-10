from typing import Any
from utils.distances import dist
from numpy import ndarray
from random import uniform

def rand(start, end): return round(uniform(start, end))

def proportional(potentialFacilities: 'ndarray[int]', args: dict[str, Any]):
  if 'competitorsQuality' not in args.keys():
    args['competitorsQuality'] = [rand(30, 80) for i in range(len(args['competitors']))]
  if 'newQuality' not in args.keys():
    args['newQuality'] = [rand(30, 80) for i in range(len(potentialFacilities))]
  attractedPopulation = 0
  for i, population in enumerate(args['population']):
    aX = 0
    aJ = 0
    for j, x in enumerate(potentialFacilities):
      aX += args['newQuality'][j] / (1 + dist(i, x, args['distance']))
    for t, j in enumerate(args['competitors']):
      aJ += args['competitorsQuality'][t] / (1 + dist(i, x, args['distance']))
    attractedPopulation += aX / (aX + aJ) * population
  return attractedPopulation