# random search - pick x random locations and return the best one
from copy import copy
from random import uniform
from typing import Any

def rand(start, end): return round(uniform(start, end))

def random(args: dict[str, Any]):
  objective = args['objective']
  bestLocationIndexes = [rand(0, len(args['candidates'])-1) for i in range(args['newCount'])]
  bestLocations = [args['candidates'][i] for i in bestLocationIndexes]
  bestValue = objective(bestLocations, args)
  for i in range(args['cycles']):
    # generate random locations
    locationIndexes = [rand(0, len(args['candidates'])-1) for i in range(args['newCount'])]
    if len(set(locationIndexes)) == len(locationIndexes):
      locations = [args['candidates'][i] for i in locationIndexes]
      # check if they are better than the best ones
      value = objective(locations, args)
      if value > bestValue:
        bestValue = value
        bestLocations = copy(locations)
  return bestLocations
