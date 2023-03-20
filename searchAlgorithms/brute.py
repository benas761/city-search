from copy import copy
from typing import Any

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
  newLocationCount = args['new']

  # saves the indexes of potential locations
  locationIndexes = [0] * newLocationCount
  cityIndexes = range(len(args['population']))
  args['newQuality'] = [args['potentialQuality'][i] for i in locationIndexes]
  bestLocations = [args['potential'][i] for i in locationIndexes]
  bestValue = objective(bestLocations, cityIndexes, args)
  i = newLocationCount - 1
  maxValueReached = False
  while locationIndexes[0] < len(args['potential']):
    if not maxValueReached and i+1 < len(locationIndexes) and locationIndexes[i+1] < len(args['potential']):
      i += 1
      continue
    locationIndexes[i] += 1
    if locationIndexes[i] < len(args['potential']):
      if len(set(locationIndexes)) == len(locationIndexes):
        locations = [args['potential'][i] for i in locationIndexes]
        args['newQuality'] = [args['potentialQuality'][i] for i in locationIndexes]
        value = objective(locations, cityIndexes, args)
        if value > bestValue:
          bestValue = value
          bestLocations = copy(locations)
    elif i != 0:
      locationIndexes[i] = 0
      i -= 1
      maxValueReached = True
      continue
    maxValueReached = False
  return bestLocations
