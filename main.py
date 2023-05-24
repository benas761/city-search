#!python
from typing import Any
import time
import numpy as np
from sys import argv
import argparse
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils.gui import drawWindow
from utils.maps import objectiveMap
from utils.distances import buildTriangleMatrix, assignNoDistances
from searchAlgorithms import bruteSubparser, randomSubparser, rdoaSubparser, rdoadSubparser
from searchAlgorithms.firmExpansion.utils import calculateCannibalism, calculatePreexistingValue

X = []

def readCompetitors(competitorFile: str):
  competitorStr = open(competitorFile, 'r').read().split('\n')
  competitors = []
  competitorsBrands = competitorStr.pop(0).split()
  for i in competitorsBrands:
    competitors.append([])
    for j in range(int(i)):
      competitors[-1].append([float(t) for t in competitorStr.pop(0).split()])
  return competitors

def main(args: dict[str, Any]):
  searchAlgorithm = args.pop('search')
  # load all cities with X, Y and population
  args['points'] = np.loadtxt(args['points'])
  args['population'] = np.array([x[2] for x in args['points']])
  args['totalPopulation'] = sum(args['population'])
  if args['noDistances']:
    assignNoDistances(args['points'])
  else:
    buildTriangleMatrix(args['points'])
  # already existing objects with the city's index and location's attractiveness
  args['competitors'] = readCompetitors(args['competitors'])
  # potential new objects
  args['candidates'] = np.loadtxt(args['candidates'])
  startTime = time.time()
  global X
  X = searchAlgorithm(args)
  print(f'Ran for {round(time.time() - startTime, 4)} seconds')
  if args['expandingFirm'] == -1:
    print(f"Chosen objects: {', '.join([str(int(x)) for x, qx in X])}")
    print(f"Captured demand: {args['objective'](X, args)}")
    X = [X]
    animate(0)
    plt.show()
  else:
    for x in X:
      demand = args['objective'](x, args)
      preexistingValue = calculatePreexistingValue(args)
      cannibalism = calculateCannibalism(args, x, preexistingValue)
      print(f"Chosen objects: {', '.join([str(int(x)) for x, qx in x])}")
      print(f"Captured demand: {demand}")
      print(f"Cannibalism effect: {cannibalism}\n")
    fig = plt.figure(figsize=(7, 5))
    animation = FuncAnimation(fig, animate, interval=3000, save_count=12)
    plt.show()

def animate(i):
  plt.clf()
  x = [j[0] for j in args['points']]
  y = [j[1] for j in args['points']]
  plt.scatter(x, y, c='b')
  # Select the point that the index of the facility X[i] points to
  idx = i % len(X)
  x = [args['points'][int(j[0])][0] for j in X[idx]]
  y = [args['points'][int(j[0])][1] for j in X[idx]]
  plt.scatter(x, y, s=50, c='r')

def parseArgs():
  parser = argparse.ArgumentParser(description='Solve an optimization problem with the chosen algorithm.')
  parser.add_argument(
    '-o', '--objective',
    required=True,
    choices=objectiveMap.keys()
  )
  parser.add_argument(
    '-e', '--expandingFirm',
    default=-1,
    type=int,
    help='The index of the competitor firm that gets treated as the expanding firm for CFLP/FE problem. Default is -1, solving for CFLP/EF'
  )
  parser.add_argument(
    '-A', '--minAttraction',
    default=0.2,
    type=float,
    help='The minimum attraction percentage of its competitors that every object has to reach. Used in proportional models'
  )
  parser.add_argument(
    '-I', '--points',
    default='data/case0/demands.dat',
    type=str,
    help='Filename of the city coordinate and population data'
  )
  parser.add_argument(
    '-J', '--competitors',
    default='data/case0/competitors.dat',
    type=str,
    help='Filename of the existing competitor facilities and their quality'
  )
  parser.add_argument(
    '-L', '--candidates',
    default='data/case0/candidates.dat',
    type=str,
    help='Filename of the planned potential new facilities and their quality'
  )
  parser.add_argument(
    '-s', '--newCount',
    default=3,
    type=int,
    help='New object count'
  )
  parser.add_argument(
    '--noDistances',
    action='store_true',
    help='Whenever to not precalculate the distances'
  )
  subparsers = parser.add_subparsers(
    title='search',
    description='Valid search algorithms'
  )
  bruteSubparser(subparsers)
  randomSubparser(subparsers)
  rdoaSubparser(subparsers)
  rdoadSubparser(subparsers)
  args = vars(parser.parse_args())
  args['objective'] = objectiveMap[args['objective']]
  return args

if __name__ == "__main__":
  args = drawWindow() if len(argv) == 1 else parseArgs()
  main(args)
