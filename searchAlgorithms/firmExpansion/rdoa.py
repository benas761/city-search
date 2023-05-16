from copy import copy
from typing import Any, Callable
from random import uniform, sample
import numpy as np

from utils.distances import dist
from searchAlgorithms.firmExpansion.utils import isDominant, calculateCannibalism, calculatePreexistingValue

# Same as checkPoint in utils, but also deals with location ranks
def checkPoint(
  Xvals: 'list[float, list[int]]',
  X: 'np.ndarray[np.ndarray[int]]', 
  Avals: 'list[list[float, list[int]]]', 
  A: 'list[np.ndarray[np.ndarray[int]]]',
  ranks: 'list[int]'
):
  i = 0
  dominatedPoints = set()
  value, cannibalism, rankIndexes = Xvals
  while i < len(Avals): # for j, (pvalue, pcannibalism) in enumerate(Pvals):))
    # if P is dominant or is the new value is already in P, the new value gets discarded
    pValue, pCannibalism, pRankIndexes = Avals[i]
    if pValue == value and pCannibalism == cannibalism:
      pass
    if isDominant(pValue, pCannibalism, value, cannibalism) or np.allclose(A[i], X):
      return A
    if isDominant(value, cannibalism, pValue, pCannibalism):
      A.pop(i)
      Avals.pop(i)
      dominatedPoints.update(pRankIndexes)
      i -= 1
    i += 1
  A.append(copy(X))
  Avals.append(copy(Xvals))
  for idx in rankIndexes:
    ranks[idx] += 1
  for idx in dominatedPoints:
    if idx not in rankIndexes:
      ranks[idx] -= 1
  return A

def rdoa(args: dict[str, Any], locationFunction: Callable):
  # take the first s potential locations
  ARankIndexes = sample(range(len(args['candidates'])), args['newCount'])
  A = [[args['candidates'][i] for i in ARankIndexes]]
  preexistingFacilityValue = calculatePreexistingValue(args)
  Avals = [
    [
      args['objective'](A[0], args), 
      calculateCannibalism(args, A[0], preexistingFacilityValue),
      ARankIndexes
    ]
  ]
  nX = []
  ranks = [1] * len(args['candidates'])
  
  for c in range(args['cycles']):
    # Select X randomly from the set of Pareto locations A
    idx = int(uniform(0, len(A)))
    Xvals = Avals[idx]
    X = copy(A[idx])
    # generating a new solution
    nXRankIndexes = []
    solutionChanged = False
    while not solutionChanged:
      nX.clear()
      nXRankIndexes.clear()
      for i, x in enumerate(X):
        if uniform(0, 1) < 1/args['newCount']:
          # select a new location
          allLocations = list(X) + nX # TODO: should all of A be excluded?
          # only use candidates that are not in the chosen locations
          newCandidates, newRanks = [], []
          for j in range(len(ranks)):
            isLocation = False
            for l in allLocations:
              if np.all(args['candidates'][j] == l):
                isLocation = True
            if not isLocation:
              newCandidates.append(args['candidates'][j])
              newRanks.append(ranks[j])
          nx = locationFunction(newCandidates, newRanks, x)
          nXRankIndex = [i for i, l in enumerate(args['candidates']) if (l == nx).all()][0]
          nX.append(nx)
          nXRankIndexes.append(nXRankIndex)
          solutionChanged = True
        else:
          nX.append(x)
          nXRankIndexes.append(Xvals[2][i])
    # get the new solution's objective function values to compare with
    nXvals = [
      args['objective'](nX, args),
      calculateCannibalism(args, nX, preexistingFacilityValue),
      nXRankIndexes
    ]
    # Add the solution to A and update ranks
    checkPoint(nXvals, nX, Avals, A, ranks)
    # recalculate the ranks according to the minimum rank value
    minRank = min(ranks)
    for i, rank in enumerate(ranks):
      if minRank < 1: ranks[i] = ranks[i] + minRank + 1
      elif minRank > 1: ranks[i] = ranks[i] - minRank + 1
  return A