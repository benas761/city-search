from copy import copy
from typing import Any, Callable
from random import uniform, sample
import numpy as np

from utils.distances import dist


def rdoa(args: dict[str, Any], locationFunction: Callable):
  # take the first s potential locations
  # X = args['candidates'][:args['newCount']]
  # take s random locations instead
  XRankIndexes = sample(range(len(args['candidates'])), args['newCount'])
  X = [args['candidates'][i] for i in XRankIndexes]

  nX = []
  nXRankIndexes = []

  ranks = [1] * len(args['candidates'])
  value = args['objective'](X, args)
  for c in range(args['cycles']):
    # new solution
    solutionChanged = False
    while not solutionChanged:
      nX.clear(); nXRankIndexes.clear()
      for i, x in enumerate(X):
        if uniform(0, 1) < 1/args['newCount']:
          # select a new location
          allLocations = list(X) + nX
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
          nXRankIndex = None
          for i, l in enumerate(args['candidates']):
            if (l == nx).all():
              nXRankIndex = i
              break
          nX.append(nx)
          nXRankIndexes.append(nXRankIndex)
          solutionChanged = True
        else:
          nX.append(x)
          nXRankIndexes.append(XRankIndexes[i])
    nValue = args['objective'](nX, args)
    if nValue > value:
      # up the new solution's ranks
      for idx in nXRankIndexes:
        ranks[idx] += 1
      # lower previous solution's ranks
      for idx in XRankIndexes:
        if idx not in nXRankIndexes:
          ranks[idx] -= 1
      # assign the new solution as best
      X = copy(nX)
      XRankIndexes = copy(nXRankIndexes)
      value = nValue
    else:
      # lower the new solution's ranks
      for idx in nXRankIndexes:
        if idx not in XRankIndexes:
          ranks[idx] -= 1
    # go through all ranks and make any worth <1 be 1
    for i, rank in enumerate(ranks):
      if rank < 1: ranks[i] = 1
  return X