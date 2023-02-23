#==============================================================================
# Implementation of the binary model of customer behavior
#==============================================================================

import math
from haversine import haversine

#==============================================================================
# Utility of the new locations given by X
#==============================================================================

def utilityBinary(I, J, X):
    
    AttrJ = []          # attractiveness of all preexisting facilities
    AttrX = []          # attractiveness of all new facilities
    utility = 0         # utility of the new facilties
    totalDemand = 0     # total demand of the whole population
    
    for i in range(0,len(I)):
        totalDemand = totalDemand + I[i,2]
        
        # Calculate AttrP
        AttrJ.clear()
        for j in range(0,len(J)):
            AttrJ.append(haversine(I[i,0], I[i,1], I[J[j],0], I[J[j],1]))
            
        # Calculate AttrX
        AttrX.clear()
        for j in range(0,len(X)):
            AttrX.append(haversine(I[i,0], I[i,1], I[X[j],0], I[X[j],1]))
        
        # If the best of AttrX is better than the best of AttrJ
        if (min(AttrX) < min(AttrJ)):
            utility = utility + I[i,2]
        
        # If the best of Attr is equal to the best of AttrJ
        elif (min(AttrX) == min(AttrJ)):
            utility = utility + I[i,2]/3
    
    return utility/totalDemand*100