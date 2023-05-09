from typing import Any
import numpy as np

# does x dominate y
def isDominant(xv: float, xc: float, yv: float, yc: float):
  return xv > yv and xc <= yc or xv == yv and xc < yc

def checkPoint(
  Xvals: list[float],
  X: 'np.ndarray[np.ndarray[int]]', 
  Pvals: 'list[list[float]]', 
  P: 'list[np.ndarray[np.ndarray[int]]]'
):
  i = 0
  value, cannibalism = Xvals
  while i < len(Pvals): # for j, (pvalue, pcannibalism) in enumerate(Pvals):))
    # if P is dominant, the new value gets discarded
    pvalue, pcannibalism = Pvals[i]
    if isDominant(pvalue, pcannibalism, value, cannibalism):
      return P
    if isDominant(value, cannibalism, pvalue, pcannibalism):
      P.pop(i)
      Pvals.pop(i)
      i -= 1
    i += 1
  P.append(X)
  Pvals.append([value, cannibalism])
  return P

# calculate the market value of the firm's preexisting facilities by removing
# them from preexisting facilities and adding them as X
def calculatePreexistingValue(args: dict[str, Any]):
  objective = args['objective']
  oldFacilities = args['competitors'].pop(args['expandingFirm'])
  preexistingFacilityValue = objective(oldFacilities, args)
  args['competitors'].insert(args['expandingFirm'], oldFacilities)
  return preexistingFacilityValue

def calculateCannibalism(args: dict[str, Any], locations: list[int], preexistingFacilityValue: float):
  objective = args['objective']
  # delete firm's facilities from pre-existing ones
  oldFacilities = args['competitors'].pop(args['expandingFirm'])
  # add the new locations as pre-existing facilities
  args['competitors'].insert(args['expandingFirm'], locations)
  # calculate value
  newValue = objective(oldFacilities, args)
  # reverse pre-existing facilities
  args['competitors'].pop(args['expandingFirm'])
  args['competitors'].insert(args['expandingFirm'], oldFacilities)
  cannibalism = preexistingFacilityValue - newValue
  return cannibalism