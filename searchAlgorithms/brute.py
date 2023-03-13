from copy import copy
from typing import Any
from argparse import _SubParsersAction, ArgumentParser

# Brute force search
# Goes through every possible new location variation and picks the best one

def addSubparser(subparsers):
  parser = subparsers.add_parser(
    'brute',
    description='Use depth-first search to check every possible combination'
  )
  parser.set_defaults(search=brute)

def brute(args: dict[str, Any]):
  objective = args['objective']
  # I = args['input']
  # J = args['competitors']
  newLocationCount = args['new']

  locations = [0] * newLocationCount
  bestLocations = [0] * newLocationCount
  bestValue = objective(bestLocations, args)
  i = newLocationCount - 1
  maxValueReached = False
  while locations[0] < len(args['population']):
    if not maxValueReached and i+1 < len(locations) and locations[i+1] < len(args['population']):
      i += 1
      continue
    locations[i] += 1
    if locations[i] < len(args['population']):
      if len(set(locations)) == len(locations):
        value = objective(locations, args)
        if value > bestValue:
          bestValue = value
          bestLocations = copy(locations)
    elif i != 0:
      locations[i] = 0
      i -= 1
      maxValueReached = True
      continue
    maxValueReached = False
  return bestLocations
