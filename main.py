import numpy
from objectiveFunctions.binarymodel import utilityBinary as objectiveFunction

def main():
  I = numpy.loadtxt('demands_LT_50.dat')
  J = [0, 1, 2, 3, 4]
  X = [0, 1, 2]
  utility = objectiveFunction(I, J, X)
  print(round(utility,4))


if __name__ == "__main__":
  main()