# random search - pick x random locations and return the best one
from copy import copy
from random import uniform
import sys
from typing import Any

def rand(start, end): return round(uniform(start, end))

def addSubparser(subparsers):
  parser = subparsers.add_parser(
    'random',
    description='Pick x random locations and return the best one'
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

  bestLocations = [rand(0, len(args['population'])) for i in range(args['new'])]
  bestValue = objective(bestLocations, args)
  for i in range(1, args['cycles']):
    # generate random locations
    locations = [rand(0, len(args['population'])-1) for i in range(args['new'])]
    # check if they are better than the best ones
    value = objective(locations, args)
    if value > bestValue:
      bestValue = value
      bestLocations = copy(locations)
  return bestLocations
