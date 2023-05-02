from typing import Any
import searchAlgorithms.enteringFirm as ef
import searchAlgorithms.firmExpansion as fe


def random(args: 'dict[str: Any]'):
  return ef.random.random(args) if args['expandingFrom'] == -1 else fe.random.random(args)

def brute(args: 'dict[str: Any]'):
  return ef.brute.brute(args) if args['expandingFrom'] == -1 else fe.brute.brute(args)

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
  parser.add_argument(
    '--cycles',
    type=int,
    default=1000,
    help='The amount of random locations to loop through'
  )
  parser.set_defaults(search=random)