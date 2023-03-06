from copy import copy
from typing import Any

# Brute force search
# Goes through every possible new location variation and picks the best one

def addSubparser(subparsers):
  parser = subparsers.add_parser(
    'greedy',
    description='Use depth-first search to check every possible combination'
  )
  parser.set_defaults(search=brute)

def brute(args: dict[str, Any]):
  objective = args['objective']
  I = args['cities']
  J = args['existing']
  newLocationCount = args['new']

  locations = [0] * newLocationCount
  bestLocations = [0] * newLocationCount
  bestValue = objective(I, J, bestLocations)
  i = newLocationCount - 1
  maxValueReached = False
  while locations[0] < len(I):
    if not maxValueReached and i+1 < len(locations) and locations[i+1] < len(I):
      i += 1
      continue
    locations[i] += 1
    if locations[i] < len(I):
      if len(set(locations)) == len(locations):
        value = objective(I, J, locations)
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
