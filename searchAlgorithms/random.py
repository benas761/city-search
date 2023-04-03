# random search - pick x random locations and return the best one
from copy import copy
from random import uniform
import sys
from typing import Any

def rand(start, end): return round(uniform(start, end))

def addSubparser(subparsers):
  parser = subparsers.add_parser(
    'random',
    description='Pick c random locations and return the best one'
  )
  parser.add_argument(
    '-c', '--cycles',
    type=int,
    default=1000,
    help='The amount of random locations to loop through'
  )
  parser.set_defaults(search=random)

def random(args: dict[str, Any]):
  objective = args['objective']

  cityIndexes = range(len(args['population']))
  bestLocationIndexes = [rand(0, len(args['potential'])-1) for i in range(args['new'])]
  bestLocations = [args['potential'][i] for i in bestLocationIndexes]
  bestValue = objective(bestLocations, cityIndexes, args)
  for i in range(1, args['cycles']):
    # generate random locations
    locationIndexes = [rand(0, len(args['potential'])-1) for i in range(args['new'])]
    if len(set(locationIndexes)) == len(locationIndexes):
      locations = [args['potential'][i] for i in locationIndexes]
      # check if they are better than the best ones
      value = objective(locations, cityIndexes, args)
      if value > bestValue:
        bestValue = value
        bestLocations = copy(locations)
  return bestLocations
