import os
import math
import time
import csv
import numpy as np
from typing import Iterable
from random import sample, uniform
from searchAlgorithms import rdoa, random, rdoa_d
from customerRules.proportional import proportional
from main import readCompetitors
from utils.distances import buildTriangleMatrix
import matplotlib.pyplot as plt

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
def searchSpeed(caseFolder: str):
  points = np.loadtxt('data/case3/demands_LT_100.dat')
  args = {
    'objective': proportional,
    'minAttraction': 0.2,
    'distance': buildTriangleMatrix(points), 
    'competitors': readCompetitors('data/case3/competitors_10.dat'),
    'candidates': np.loadtxt('data/case3/candidates_50.dat'),
    'expandingFirm': -1,
    'newCount': 3,
    'noDistances': False,
    'population': [i[2] for i in points],
    'totalPopulation': sum([i[2] for i in points]),
    'loggingLevel': 'info',
    'search': random,
    'cycles': 1
  }
  searches = [
    (random, 'random'),
    (rdoa, 'rdoa'),
    (rdoa_d, 'rdoa-d')
  ]
  for search, searchName in searches:
    file = open(f"output/{searchName}Speed.csv", 'w', newline='')
    writer = csv.DictWriter(file, ['cycles', 'value', 'time'])
    writer.writeheader()
    
    args['search'] = search
    for cycles in range(10, 101, 10):
      for repeat in range(1000):
        args['cycles'] = cycles
        startTime = time.time()
        X = args['search'](args)
        searchTime = round(time.time() - startTime, 4)
        row = {
          'cycles': cycles,
          'value': round(args['objective'](X, args), 4),
          'time': searchTime
        }
        print(row)
        writer.writerow(row)
    file.close()

def visualiseAccuracy(files: Iterable[str], algorithmNames: Iterable[str]):
  if len(files) != len(algorithmNames):
    raise ValueError('Each file must have a corresponding algorithm name')
  allCycles = set()
  csvReaders = []
    # expects csv files with at least keys 'cycles' and 'value' in their header
  for fileName in files:
    file = open(fileName, 'r')
    csvReader = list(csv.DictReader(file))
    allCycles.update({row['cycles'] for row in csvReader})
    csvReaders.append(csvReader)
  
  allCycles = list(allCycles)[:2]
  figure, plots = plt.subplots(1, len(allCycles))
  readerCycleValues = []
  for i, cycle in enumerate(allCycles):
    # x - value
    # y - chance to get it for one
    for csvReader in csvReaders:
      readerCycleValues.append([
        float(row['value']) for row in csvReader
        if row['cycles'] == cycle
      ])
    # maximum value of the worst performing algorithm is 
    # used as a base for further probability calculation
    lines = []
    maxValue = max([max(values) for values in readerCycleValues])
    minValue = min([min(values) for values in readerCycleValues])
    for cycleValues, name in zip(readerCycleValues, algorithmNames):
      x = np.linspace(0.0, 1.0, 20)
      y = []
      distribution = np.linspace(minValue, maxValue, 20)
      for dval in distribution:
        count = len([val for val in cycleValues if int(val) >= dval])
        y.append(count/len(cycleValues))
      line, = plots[i].plot(x, y, label=name)
      lines.append(line)
    plots[i].legend(handles=lines, loc='upper right', fontsize='small')
  plt.show()
  

if __name__ == "__main__":
  os.makedirs('./output', exist_ok=True)
  # visualiseAccuracy([
  #   'output/1000 city speeds/randomSpeed.csv',
  #   'output/1000 city speeds/rdoa-dSpeed.csv',
  #   'output/1000 city speeds/rdoaSpeed.csv'
  # ], [
  #   'PRS', 'RDOA-D', 'RDOA'
  # ])
  # camelTest()
  # citySpeed()
  searchSpeed('case3')
  # generateObjects("data/case3/candidates_50.dat", 50, 100)