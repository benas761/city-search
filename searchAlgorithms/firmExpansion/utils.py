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
  for pvalue, pcannibalism in Pvals:
    # if P is dominant, X goes away and the same arr gets returned
    if isDominant(pvalue, pcannibalism, value, cannibalism):
      return P
    elif isDominant(value, cannibalism, pvalue, pcannibalism):
      P.pop(i)
      Pvals.pop(i)
      i -= 1
    i += 1
  P.append(X)
  Pvals.append([value, cannibalism])
  return P

def calculateCannibalism(args: dict[str, Any], locations: list[int]):
  objective = args['objective']
  # delete firm's facilities from pre-existing ones
  oldFacilities = args['competitors'].pop(args['expandingFirm'])
  # calculate their value
  oldValue = objective(oldFacilities, args)
  # add the new locations as pre-existing facilities
  args['competitors'].insert(args['expandingFirm'], locations)
  # calculate value
  newValue = objective(oldFacilities, args)
  # reverse pre-existing facilities
  args['competitors'].pop(args['expandingFirm'])
  args['competitors'].insert(args['expandingFirm'], oldFacilities)
  cannibalism = oldValue - newValue
  return cannibalism