from typing import Any
import searchAlgorithms.enteringFirm as ef
import searchAlgorithms.firmExpansion as fe


def random(args: 'dict[str: Any]'):
  return ef.random.random(args) if args['expandingFirm'] == -1 else fe.random.random(args)

def brute(args: 'dict[str: Any]'):
  return ef.brute.brute(args) if args['expandingFirm'] == -1 else fe.brute.brute(args)

def rdoa(args: 'dict[str: Any]'):
  if args['expandingFirm'] == -1:
    return ef.rdoa.rdoa(args, ef.rdoaRankingLocation)
  else:
    return fe.rdoa.rdoa(args, ef.rdoaDistanceLocation)

def rdoa_d(args: 'dict[str: Any]'):
  if args['expandingFirm'] == -1:
    return ef.rdoa.rdoa(args, ef.rdoaDistanceLocation)
  else:
    return fe.rdoa.rdoa(args, ef.rdoaRankingLocation)

def addCycles(parser):
  parser.add_argument(
    '--cycles',
    type=int,
    default=1000,
    help='The amount of random locations to loop through'
  )


def bruteSubparser(subparsers):
  parser = subparsers.add_parser(
    'brute',
    description='Use depth-first search to check every possible combination'
  )
  parser.set_defaults(search=brute)

def randomSubparser(subparsers):
  parser = subparsers.add_parser(
    'random',
    description='Pick c random locations and return the best one'
  )
  addCycles(parser)
  parser.set_defaults(search=random)

def rdoaSubparser(subparsers):
  parser = subparsers.add_parser(
    'rdoa',
    description='Ranking-based discrete optimisation algorithm (RDOA)'
  )
  addCycles(parser)
  parser.set_defaults(search=rdoa)

def rdoadSubparser(subparsers):
  parser = subparsers.add_parser(
    'rdoa-d',
    description='Ranking-based discrete optimisation algorithm with distance ranking (RDOA-D)'
  )
  addCycles(parser)
  parser.set_defaults(search=rdoa_d)