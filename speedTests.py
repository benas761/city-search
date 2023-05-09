import math
import time
import csv
import numpy as np
from random import sample, uniform
from searchAlgorithms import rdoa, random, rdoa_d
from objectiveFunctions.proportional import proportional
from main import readCompetitors
from utils.distances import buildTriangleMatrix

def generateObjects(filename: str, objectCount: int, cityCount: int):
  file = open(filename, 'w')
  locationIndexes = sample(range(cityCount), objectCount)
  file.writelines([
    f"{idx} {round(uniform(30, 80))}\n"
    for idx in locationIndexes
  ])
  file.close()

# test how long algorithms take with an increasing number of cities
def citySpeed():
  points = np.loadtxt('data/demands_LT_12395.dat')
  args = {
    'objective': proportional,
    'minAttraction': 0.2,
    'distance': [], 
    'competitors': readCompetitors('data/competitors_4.dat'),
    'candidates': np.loadtxt('data/potentialLocations_12.dat'),
    'expandingFirm': -1,
    'newCount': 3,
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

# how accurate the algorithms are with different amounts of cycles and locations
def searchSpeed():
  points = np.loadtxt('data/demands_LT_12395.dat')
  args = {
    'objective': proportional,
    'minAttraction': 0.2,
    'distance': buildTriangleMatrix(points), 
    'competitors': readCompetitors('data/case1/competitors_10.dat'),
    'candidates': np.loadtxt('data/case1/candidates_500.dat'),
    'expandingFirm': -1,
    'newCount': 5,
    'noDistances': False,
    'population': [i[2] for i in points],
    'totalPopulation': sum([i[2] for i in points]),
    'loggingLevel': 'info',
    'search': random,
    'cycles': 1
  }
  resultsFile = open('output/searchSpeed.csv', 'w')
  writer = csv.DictWriter(resultsFile, ['search', 'cycles', 'value', 'time'])
  writer.writeheader()
  searches = [
    (random, 'random'),
    (rdoa, 'rdoa'),
    (rdoa_d, 'rdoa-d')
  ]
  # for cycles in range(1000, 5001, 1000):
  for cycles in [20]:
    args['cycles'] = cycles
    for search, searchName in searches:
      args['search'] = search
      startTime = time.time()
      X = args['search'](args)
      searchTime = round(time.time() - startTime, 4)
      row = {
        'search': searchName,
        'cycles': cycles,
        'value': args['objective'](X, args),
        'time': searchTime
      }
      print(row)
      writer.writerow(row)

# how long they take with an increasing number of objects on a smaller amount of cities
 
if __name__ == "__main__":
  # citySpeed()
  searchSpeed()
  # generateObjects("data/case1/candidates_500.dat", 500, 12395)