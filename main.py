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
# validate args
# put algorithms into classes
# time logging
# logging
# visuals

def main(args: dict[str, Any]):
  searchAlgorithm = args.pop('search')
  # load all cities with X, Y and population
  args['input'] = np.loadtxt(args['input'])
  args['population'] = np.array([x[2] for x in args['input']])
  args['distance'] = args.pop('input') if args['noDistances'] else buildTriangleMatrix(args.pop('input'))
  # already existing objects with the city's index and location's attractiveness
  args['existing'] = [0, 1, 2, 3, 4]
  # potential new objects, need to be found'
  startTime = time.time()
  X = searchAlgorithm(args)
  print(f'Ran for {round(time.time() - startTime, 4)} seconds')
  print(X)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Solve an optimization problem with the chosen algorithm.')
  objectiveMap = {
    'binary': binary,
    'proportional': proportional
  }
  # searchMap = {
  #   'brute': brute,
  #   'random': random
  # }
  parser.add_argument(
    '-o', '--objective',
    required=True,
    choices=objectiveMap.keys()
  )
  # parser.add_argument(
  #   '-s', '--search',
  #   required=True,
  #   choices=searchMap.keys()
  # )
  parser.add_argument(
    '-i', '--input',
    default='data/demands_LT_50.dat',
    type=str,
    help='Filename of the city coordinate and population data'
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