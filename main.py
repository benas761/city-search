#!python
from typing import Any
import numpy
import argparse
from objectiveFunctions.binarymodel import binary
from searchAlgorithms.brute import addSubparser as addBruteSubparser

# TODO: 
# validate args
# put algorithms into classes
# time logging
# logging
# visuals

def main(args: dict[str, Any]):
  # all cities with X, Y and population
  args['cities'] = numpy.loadtxt(args['cities'])
  # already existing objects with the city's index and location's attractiveness
  args['existing'] = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]
  # potential new objects, need to be found
  searchAlgorithm = args.pop('search')
  validate(args)

  X = searchAlgorithm(args)
  print(X)

def validate(args: dict[str, Any]):
  # if the new objects cannot be placed in the same city, the existing cities must be plenty enough 
  if len(args['cities']) < len(args['new']):
    raise ValueError('There must be enough cities for new locations')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Solve an optimization problem with the chosen algorithm.')
  objectiveMap = {
    'binary': binary
  }
  parser.add_argument(
    '-o', '--objective',
		required=True,
    choices=objectiveMap.keys()
  )
  parser.add_argument(
    '-c', '--cities',
		required=True,
		type=str,
    help='Filename of the city coordinate and population data'
  )
  parser.add_argument(
    '-n', '--new',
		required=True,
		type=int,
    help='New object count'
  )
  # parser.add_argument(
  #   '-v', '--visualise',
  #   help='A flag for visualization of the algorithm'
  # )
  subparsers = parser.add_subparsers(
    title='Algorithms',
    description='Valid search algorithms',
    help='Choose the algorithm to execute'
  )
  addBruteSubparser(subparsers)
  args = vars(parser.parse_args())
  args['objective'] = objectiveMap[args['objective']]
  main(args)