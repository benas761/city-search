from random import uniform

from utils.distances import dist
from . import brute, random, rdoa

# location choice methods split by their probablility calculation
# for RDOA:
def rdoaRankingLocation(candidates, ranks, currentLocation):
  i = 0
  # run until you find a candidate, even if one isn't found after checking all candidates
  while True:
    idx = i % len(candidates)
    probability = ranks[idx] / sum(ranks)
    if uniform(0, 1) < probability:
      return candidates[idx]
    i += 1

# for RDOA-D
def rdoaDistanceLocation(candidates, ranks, currentLocation):
  i = 0
  # run until you find a candidate, even if one isn't found after checking all candidates
  while True:
    idx = i % len(candidates)
    distRankSum = sum([
      ranks[j]/dist(currentLocation[0], candidates[j][0])
      for j in range(len(candidates))
    ])
    probability = ranks[idx] / (dist(currentLocation[0], candidates[idx][0]) * distRankSum)
    if uniform(0, 1) < probability:
      return candidates[idx]
    i += 1