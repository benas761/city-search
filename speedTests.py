import math
import time
import csv
import numpy as np
from searchAlgorithms.enteringFirm.random import random
from objectiveFunctions.proportional import proportional
from main import readCompetitors
from utils.distances import buildTriangleMatrix

# test how long algorithms take with an increasing number of cities
def citySpeed():
  points = np.loadtxt('data/demands_LT_12395.dat')
  args = {
    'objective': proportional,
    'minAttraction': 0.2,
    'distance': [], 
    'competitors': readCompetitors('data/competitors_4.dat'),
    'potential': np.loadtxt('data/potentialLocations_12.dat'),
    'new': 3,
    'noDistances': False,
    'population': [],
    'totalPopulation': sum([i[2] for i in points]),
    'loggingLevel': 'debug',
    'search': random,
    'cycles': 1
  }
  resultsFile = open('output/citySpeed.csv', 'w')
  writer = csv.DictWriter(resultsFile, ['n', 'Distance matrix', 'Search', 'Market capture'])
  writer.writeheader()
  runCycles = 4
  n = math.trunc(len(points)/2**runCycles)
  while n < len(points):
    startTime = time.time()
    args['distance'] = buildTriangleMatrix(points[:n])
    matrixBuildTime = round(time.time() - startTime, 4)
    args['population'] = np.array([p[2] for p in points[:n]])
    args['totalPopulation'] = sum(args['population'])
    startTime = time.time()
    X = args['search'](args)
    searchTime = round(time.time() - startTime, 4)
    row = {
      'n': n,
      'Distance matrix': matrixBuildTime,
      'Search': searchTime,
      'Market capture': round(args['objective'](X, range(len(args['population'])), args), 3)
    }
    print(row)
    writer.writerow(row)
    n *= 2
# how long they take with an increasing number of objects on a smaller amount of cities
 
if __name__ == "__main__":
  citySpeed()