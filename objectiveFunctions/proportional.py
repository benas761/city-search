from utils.distances import dist
from random import uniform

def rand(start, end): return round(uniform(start, end))

# def proportional(I, J, X, qJ = None, qX = None):
def proportional(potentialFacilities, args):
  # TODO: read quality metrics from file
  if 'existingQuality' not in args.keys():
    qJ = [rand(30, 80) for i in range(len(args['existing']))]
  if 'newQuality' not in args.keys():
    qX = [rand(30, 80) for i in range(len(potentialFacilities))]
  attractedPopulation = 0
  for i, population in enumerate(args['population']):
    aX = 0
    aJ = 0
    for j, x in enumerate(potentialFacilities):
      aX += qX[j] / (1 + dist(i, x, args['distance']))
    for t, j in enumerate(args['existing']):
      aJ += qJ[t] / (1 + dist(i, x, args['distance']))
    attractedPopulation += aX / (aX + aJ) * population
  return attractedPopulation