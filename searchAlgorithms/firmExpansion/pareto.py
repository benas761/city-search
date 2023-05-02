import numpy as np

# does x dominate y
def isDominant(xv: float, xc: float, yv: float, yc: float):
  return xv > yv and xc <= yc or xv >= yv and xc < yc

def checkPoint(value: float, cannibalism: float, X: 'np.ndarray[np.ndarray[int]]', P: 'list[list[float, np.ndarray[np.ndarray[int]]]]'):
  for i, (pvalue, pcannibalism, pX) in enumerate(P):
    # if P is dominant, X goes away and the same arr gets returned
    if isDominant(pvalue, pcannibalism, value, cannibalism):
      return P
    elif isDominant(value, cannibalism, pvalue, pcannibalism):
      P.pop(i)
  P.append([value, cannibalism, X])
  return P