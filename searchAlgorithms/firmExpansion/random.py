# random search - pick x random locations and return the best one
from copy import copy
from random import uniform
from typing import Any
from searchAlgorithms.firmExpansion.pareto import checkPoint

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
  for i in range(args['cycles']):
    # generate random locations
    locationIndexes = [rand(0, len(args['potential'])-1) for i in range(args['newCount'])]
    if len(set(locationIndexes)) == len(locationIndexes):
      locations = [args['potential'][i] for i in locationIndexes]
      # check if they are better than the best ones
      # TODO: make competitors be an ndarray
      value = objective(locations, args)
      # delete firm's facilities from pre-existing ones
      args['competitors'] = list(args['competitors'])
      oldFacilities = args['competitors'].pop(args['expandingFrom'])
      # calculate their value
      oldValue = objective(oldFacilities, args)
      # add the new locations as pre-existing facilities
      args['competitors'].insert(args['expandingFrom'], locations)
      # calculate value
      newValue = objective(oldFacilities, args)
      # reverse pre-existing facilities
      args['competitors'].pop(args['expandingFrom'])
      args['competitors'].insert(args['expandingFrom'], oldFacilities)
      cannibalism = oldValue - newValue
      # append to bestLocations if the point is pareto optimal
      checkPoint(value, cannibalism, locations, bestLocations)
  return bestLocations
