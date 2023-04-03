from typing import Any
from utils.distances import dist
from numpy import ndarray

def binary(potentialFacilities: 'ndarray[int]', capturedObjects: list[int], args: dict[str, Any]):
    if len(capturedObjects) == 0: return 0

    AttrJ = []          # attractiveness of all preexisting facilities
    AttrX = []          # attractiveness of all new facilities
    utility = 0         # utility of the new facilties
    totalDemand = 0     # total demand of the whole population
    
    for i in capturedObjects:
        totalDemand = totalDemand + args['population'][i]
        
        # Calculate AttrP
        AttrJ.clear()
        for j, qj in args['competitors']:
            AttrJ.append(dist(i, j, args['distance']))
            
        # Calculate AttrX
        AttrX.clear()
        for x, qx in potentialFacilities:
            AttrX.append(dist(i, j, args['distance']))
        
        minX = min(AttrX)
        minJ = min(AttrJ)

        # If the best of AttrX is better than the best of AttrJ
        if (minX < minJ):
            utility = utility + args['population'][i]
        
        # If the best of Attr is equal to the best of AttrJ
        elif (minX == minJ):
            n = 0
            for x in AttrX:
                if x == minX: n += 1
            for j in AttrJ:
                if j == minX: n += 1
            utility = utility + args['population'][i]/n

    return utility/args['totalPopulation']*100