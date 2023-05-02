#!python
import logging
from typing import Any
import time
import numpy as np
import argparse
from utils.distances import buildTriangleMatrix, assignNoDistances
from objectiveFunctions.binary import binary
from objectiveFunctions.proportional import paretoProportional, proportional, partiallyProportional
from searchAlgorithms import bruteSubparser, randomSubparser

def readCompetitors(competitorFile: str):
  competitorStr = open(competitorFile, 'r').read().split('\n')
  competitors = []
  competitorsBrands = competitorStr.pop(0).split()
  for i in competitorsBrands:
    competitors.append([])
    for j in range(int(i)):
      competitors[-1].append([float(t) for t in competitorStr.pop(0).split()])
  return np.array(competitors)

def main(args: dict[str, Any]):
  logging.basicConfig(level=args['loggingLevel'].upper())
  searchAlgorithm = args.pop('search')
  args['expandingFrom'] = 0
  # load all cities with X, Y and population
  args['points'] = np.loadtxt(args['points'])
  args['population'] = np.array([x[2] for x in args['points']])
  args['totalPopulation'] = sum(args['population'])
  args['distance'] = assignNoDistances(args.pop('points')) if args['noDistances'] else buildTriangleMatrix(args.pop('points'))
  # already existing objects with the city's index and location's attractiveness
  args['competitors'] = readCompetitors(args['competitors'])
  # potential new objects
  args['potential'] = np.loadtxt(args['potential'])
  startTime = time.time()
  X = searchAlgorithm(args)
  logging.debug(f'Ran for {round(time.time() - startTime, 4)} seconds')
  logging.info(f"Chosen objects: {', '.join([str(x) for x, qx in X])}")
  logging.info(f"Captured demand: {args['objective'](X, range(len(args['population'])), args)}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Solve an optimization problem with the chosen algorithm.')
  objectiveMap = {
    'binary': binary,
    'proportional': proportional,
    'partiallyProportional': partiallyProportional,
    'paretoProportional': paretoProportional
  }
  parser.add_argument(
    '-o', '--objective',
    required=True,
    choices=objectiveMap.keys()
  )
  parser.add_argument(
    '-A', '--minAttraction',
    default=0.2,
    help='The minimum attraction percentage of its competitors that every object has to reach. Used in proportional models'
  )
  parser.add_argument(
    '-I', '--points',
    default='data/demands_LT_50.dat',
    type=str,
    help='Filename of the city coordinate and population data'
  )
  parser.add_argument(
    '-J', '--competitors',
    default='data/competitors_4.dat',
    type=str,
    help='Filename of the existing competitor facilities and their quality'
  )
  parser.add_argument(
    '-L', '--potential',
    default='data/potentialLocations_12.dat',
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
  parser.add_argument(
    '--loggingLevel',
    default='debug',
    choices=['debug', 'info', 'warning', 'error', 'critical']
  )
  subparsers = parser.add_subparsers(
    title='search',
    description='Valid search algorithms'
  )
  bruteSubparser(subparsers)
  randomSubparser(subparsers)
  args = vars(parser.parse_args())
  args['objective'] = objectiveMap[args['objective']]
  main(args)

# add a number which pre-existing firm's facilities are
# if the number is -1, solve the usual
# else, validate that the firm and extra competitors exist and redirect to other search algorithms
