#!python
from typing import Any
import time
import numpy as np
import argparse
from utils.distances import buildTriangleMatrix
from objectiveFunctions.binary import binary
from objectiveFunctions.proportional import proportional
from searchAlgorithms.brute import brute, addSubparser as bruteSubparser
from searchAlgorithms.random import random, addSubparser as randomSubparser

# TODO: 
# set up venv

def main(args: dict[str, Any]):
  searchAlgorithm = args.pop('search')
  # load all cities with X, Y and population
  args['input'] = np.loadtxt(args['input'])
  args['population'] = np.array([x[2] for x in args['input']])
  args['distance'] = args.pop('input') if args['noDistances'] else buildTriangleMatrix(args.pop('input'))
  # already existing objects with the city's index and location's attractiveness
  args['competitors'] = np.loadtxt(args['competitors'])
  args['competitorsQuality'] = [x[1] for x in args['competitors']]
  args['competitors'] = [x[0] for x in args['competitors']]
  # potential new objects, need to be found'
  startTime = time.time()
  X = searchAlgorithm(args)
  print(f'Ran for {round(time.time() - startTime, 4)} seconds')
  print(X, args['objective'](X, args))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Solve an optimization problem with the chosen algorithm.')
  objectiveMap = {
    'binary': binary,
    'proportional': proportional
  }
  parser.add_argument(
    '-o', '--objective',
    required=True,
    choices=objectiveMap.keys()
  )
  parser.add_argument(
    '-i', '--input',
    default='data/demands_LT_50.dat',
    type=str,
    help='Filename of the city coordinate and population data'
  )
  parser.add_argument(
    '-c', '--competitors',
    default='data/competitors_3.dat',
    type=str,
    help='Filename of the existing competitor facilities and their quality'
  )
  parser.add_argument(
    '-n', '--new',
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
  args = vars(parser.parse_args())
  args['objective'] = objectiveMap[args['objective']]
  main(args)