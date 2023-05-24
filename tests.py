import os
from statistics import mean
import time
import argparse
import csv
import numpy as np
from typing import Iterable
from random import sample, uniform
from utils.maps import searchMap
from customerRules.binary import binary
from main import readCompetitors
from utils.distances import buildTriangleMatrix
import matplotlib.pyplot as plt

def generateFiles(args):
  file, objectCount, cityCount = open(args['name'], 'w'), args['count'], args['max']
  locationIndexes = sample(range(cityCount), objectCount)
  file.writelines([
    f"{idx} {round(uniform(30, 80))}\n"
    for idx in locationIndexes
  ])
  file.close()

# how accurate the algorithms are with different amounts of cycles and locations
def algorithmTest(cmdArgs):
  caseFolder, algorithms = cmdArgs['case'], cmdArgs['algorithms']
  cycleCounts, repeats = cmdArgs['cycles'], cmdArgs['repeats']

  points = np.loadtxt(f'data/{caseFolder}/demands.dat')
  searches = [(searchMap[alg], alg) for alg in algorithms]
  args = {
    'objective': binary,
    'minAttraction': 0.2,
    'competitors': readCompetitors(f'data/{caseFolder}/competitors.dat'),
    'candidates': np.loadtxt(f'data/{caseFolder}/candidates.dat'),
    'expandingFirm': -1,
    'newCount': 5,
    'noDistances': False,
    'population': [i[2] for i in points],
    'totalPopulation': sum([i[2] for i in points]),
  }
  buildTriangleMatrix(points)

  for search, searchName in searches:
    os.makedirs(f"./output/{caseFolder}", exist_ok=True)
    file = open(f"output/{caseFolder}/{searchName}.csv", 'w', newline='')
    writer = csv.DictWriter(file, ['cycles', 'value', 'time'])
    writer.writeheader()
    
    args['search'] = search
    for cycles in cycleCounts:
      for repeat in range(repeats):
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

def readFolder(folder: str):
  folder = args['folder']
  files = []
  for (dirpath, dirnames, filenames) in os.walk(folder):
    files.extend(filenames)
    break
  fileLabels = [file[:-4] for file in files]
  return files, fileLabels

def visualiseProbability(args):
  files, fileLabels = readFolder(args['folder'])
  allCycles = set()
  csvReaders = []
  # expects csv files with at least keys 'cycles' and 'value' in their header
  for fileName in files:
    file = open(f"{args['folder']}/{fileName}", 'r')
    csvReader = list(csv.DictReader(file))
    allCycles.update({int(row['cycles']) for row in csvReader})
    csvReaders.append(csvReader)
  
  allCycles = list(allCycles)
  allCycles.sort()
  figure, plots = plt.subplots(1, len(allCycles))
  for i, cycle in enumerate(allCycles):
    readerCycleValues = []
    for csvReader in csvReaders:
      readerCycleValues.append([
        float(row['value']) for row in csvReader
        if int(row['cycles']) == cycle
      ])
    # maximum value of the worst performing algorithm is 
    # used as a base for further probability calculation
    lines = []
    maxValue = max([max(values) for values in readerCycleValues])
    minValue = min([min(values) for values in readerCycleValues])
    for cycleValues, name in zip(readerCycleValues, fileLabels):
      x = np.linspace(0.0, 1.0, 100)
      y = []
      distribution = np.linspace(minValue, maxValue, 100)
      for dval in distribution:
        count = len([val for val in cycleValues if float(val) >= dval])
        y.append(count/len(cycleValues))
      line, = plots[i].plot(x, y, label=name)
      plots[i].set_title(cycle)
      lines.append(line)
    plots[i].legend(handles=lines, loc='lower left', fontsize='small')
  plt.tight_layout()
  plt.show()

def visualiseAccuracy(args):
  files, fileLabels = readFolder(args['folder'])
  lines = []
  for fileName, label in zip(files, fileLabels):
    file = open(f"{args['folder']}/{fileName}", 'r')
    csvReader = list(csv.DictReader(file))
    cycles = list({int(row['cycles']) for row in csvReader})
    cycles.sort()
    x = cycles
    y = []
    for cycle in cycles:
      values = [float(row['value']) for row in csvReader if int(row['cycles']) == cycle]
      y.append(mean(values))
    line, = plt.plot(x, y, label=label)
    lines.append(line)
  plt.legend(handles=lines, loc='best', fontsize='medium')
  plt.xlabel('Ciklai')
  plt.ylabel('Užimta rinkos dalis (%)')
  plt.tight_layout()
  plt.show()
  return

# subparsers
def fileGeneratorParser(subparsers):
  parser = subparsers.add_parser(
    'generateFiles',
    description='Generate a file with random qualities and indexes for competitors or candidates'
  )
  parser.add_argument(
    '-n', '--name',
    required=True,
    help='The relative path and name of the file to generate'
  )
  parser.add_argument(
    '-c', '--count',
    type=int,
    default=5,
    help='The number of values to generate'
  )
  parser.add_argument(
    '-m', '--max',
    type=int,
    default=50,
    help='The maximum allowed index; must be less than the amount of demand points'
  )
  parser.set_defaults(function=generateFiles)

def searchTestParser(subparsers):
  parser = subparsers.add_parser(
    'algorithmTest',
    description='Test algorithm speeds and write the results into csv files'
  )
  parser.add_argument(
    '--case',
    required=True,
    help='The folder in data/ that contains demand locations as well as competitor and candidate indexes'
  )
  parser.add_argument(
    '-c', '--cycles',
    required=True,
    nargs='+',
    help='The number of cycles that the algorithms will loop through'
  )
  parser.add_argument(
    '-a', '--algorithms',
    nargs='+',
    help='Algoritms to test'
  )
  parser.add_argument(
    '-r', '--repeats',
    default=200,
    help='The number of times every cycle calculation will be repeated'
  )
  parser.set_defaults(function=algorithmTest)

def setVisualiserArgs(parser):
  parser.add_argument(
    '-f', '--folder',
    required=True,
    help='The path to the folder containing output files of the searchTest'
  )

def probabilityVisualiserParser(subparsers):
  parser = subparsers.add_parser(
    'visualiseProbability',
    description='Visualise the probabilities of finding every solution value'
  )
  setVisualiserArgs(parser)
  parser.set_defaults(function=visualiseProbability)

def accuracyVisualiserParser(subparsers):
  parser = subparsers.add_parser(
    'visualiseAccuracy',
    description='Visualise the average values of algorithms'
  )
  setVisualiserArgs(parser)
  parser.set_defaults(function=visualiseAccuracy)


if __name__ == "__main__":
  os.makedirs('./output', exist_ok=True)
  parser = argparse.ArgumentParser(description='Run a test function.')
  subparsers = parser.add_subparsers(
    title='function',
    description='A test function to be run',
    required=True
  )
  fileGeneratorParser(subparsers)
  searchTestParser(subparsers)
  probabilityVisualiserParser(subparsers)
  accuracyVisualiserParser(subparsers)
  args = vars(parser.parse_args())
  args['function'](args)
