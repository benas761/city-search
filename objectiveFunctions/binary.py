from typing import Any
from utils.distances import dist
from numpy import ndarray

def binary(potentialFacilities: 'ndarray[int]', args: dict[str, Any]):
    AttrJ = []          # attractiveness of all preexisting facilities
    AttrX = []          # attractiveness of all new facilities
    utility = 0         # utility of the new facilties
    totalDemand = 0     # total demand of the whole population
    
    for i in range(len(args['population'])):
        totalDemand = totalDemand + args['population'][i]
        AttrJ.clear()
        for firm in args['competitors']:
            for j, qj in firm:
                AttrJ.append(dist(i, j))  
        AttrX.clear()
        for x, qx in potentialFacilities:
            AttrX.append(dist(i, j))
        minX = min(AttrX)
        minJ = min(AttrJ)

        # If the best of X is better than the best of J, 
        # the best X captures the entire demand of i
        if minX < minJ:
            utility += args['population'][i]
        # If the best of Attr is equal to the best of AttrJ, 
        # the best facilities split the demand evenly
        elif minX == minJ:
            n = 0
            nx = 0
            for x in AttrX:
                if x == minX: 
                    n += 1
                    nx += 1
            for j in AttrJ:
                if j == minX: n += 1
            utility += args['population'][i]*nx/n
    return utility/args['totalPopulation']*100