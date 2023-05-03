# random search - pick x random locations and return the best one
from copy import copy
from random import uniform
from typing import Any
from searchAlgorithms.firmExpansion.utils import calculateCannibalism, checkPoint

def rand(start, end): return round(uniform(start, end))

def addSubparser(subparsers):
  parser = subparsers.add_parser(
    'random',
    description='Pick c random locations and return the best one'
  )
  parser.add_argument(
    '--cycles',
    type=int,
    default=1000,
    help='The amount of random locations to loop through'
  )
  parser.set_defaults(search=random)

def random(args: dict[str, Any]):
  objective = args['objective']
  bestLocations = []
  bestValues = []
  for i in range(args['cycles']):
    # generate random locations
    locationIndexes = [rand(0, len(args['potential'])-1) for i in range(args['newCount'])]
    if len(set(locationIndexes)) == len(locationIndexes):
      locations = [args['potential'][i] for i in locationIndexes]
      value = objective(locations, args)
      cannibalism = calculateCannibalism(args, locations)
      # append to bestLocations if the point is pareto optimal
      checkPoint([value, cannibalism], locations, bestValues, bestLocations)
  return bestLocations
