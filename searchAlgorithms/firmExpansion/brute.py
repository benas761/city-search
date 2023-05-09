from typing import Any
from searchAlgorithms.firmExpansion.utils import calculateCannibalism, checkPoint, calculatePreexistingValue

# Brute force search
# Goes through every possible new location variation and picks the best one

def brute(args: dict[str, Any]):
  objective = args['objective']
  preexistingFacilityValue = calculatePreexistingValue(args)
  newLocationCount = args['newCount']
  # saves the indexes of potential locations
  locationIndexes = [0] * newLocationCount
  bestLocations = []
  bestValues = []
  i = newLocationCount - 1
  maxValueReached = False
  while locationIndexes[0] < len(args['candidates']):
    if not maxValueReached and i+1 < len(locationIndexes) and locationIndexes[i+1] < len(args['candidates']):
      i += 1
      continue
    locationIndexes[i] += 1
    if locationIndexes[i] < len(args['candidates']):
      if len(set(locationIndexes)) == len(locationIndexes):
        locations = [args['candidates'][i] for i in locationIndexes]
        value = objective(locations, args)
        cannibalism = calculateCannibalism(args, locations, preexistingFacilityValue)
        # append to bestLocations if the point is pareto optimal
        checkPoint([value, cannibalism], locations, bestValues, bestLocations)
    elif i != 0:
      locationIndexes[i] = 0
      i -= 1
      maxValueReached = True
      continue
    maxValueReached = False
  return bestLocations
