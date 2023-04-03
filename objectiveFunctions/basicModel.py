from typing import Any
from utils.distances import dist
from objectiveFunctions.proportional import proportional
from objectiveFunctions.binary import binary
from numpy import ndarray



def basicModel(potentialFacilities: 'ndarray[int]', capturedObjects: list[int], args: dict[str, Any]):
  captureByProportion = []
  captureFull = []
  captureByBinary = []
  # TODO: add minimum attraction to the cities
  minAttraction = 2
  for i in capturedObjects: 
    attrJ = []; attrX = []
    for j, qj in args['competitors']:
      attrJ.append(qj / (1 + dist(i, j, args['distance'])))
    for x, qx in potentialFacilities:
      attrX.append(qx / (1 + dist(i, x, args['distance'])))
    maxJ = max(attrJ)
    maxX = max(attrX)
    if maxX > minAttraction and maxJ > minAttraction:
      captureByProportion.append(i)
    elif maxJ < minAttraction and maxX >= minAttraction or maxX > maxJ and maxX < minAttraction:
      captureFull.append(i)
    elif maxX < minAttraction and maxX == maxJ:
      captureByBinary.append(i)
  return \
    proportional(potentialFacilities, captureByProportion, args) + \
    sum([args['population'][i] for i in captureFull])/args['totalPopulation']*100 + \
    binary(potentialFacilities, captureByBinary, args) # TODO: change this to return the condition of equal w/out any extra checks