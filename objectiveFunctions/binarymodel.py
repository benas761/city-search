#==============================================================================
# Implementation of the binary model of customer behavior
#==============================================================================

from haversine import haversine

def addSubparser(subparsers):
  parser = subparsers.add_parser(
    'binary',
    description='Take all population that is closest to the object'
  )
  parser.set_defaults(objective=binary)

#==============================================================================
# Utility of the new locations given by X
# it will take all population, that the object is closest to
#==============================================================================

def binary(I, J, X):
    
    AttrJ = []          # attractiveness of all preexisting facilities
    AttrX = []          # attractiveness of all new facilities
    utility = 0         # utility of the new facilties
    totalDemand = 0     # total demand of the whole population
    
    for i in range(0,len(I)):
        totalDemand = totalDemand + I[i,2]
        
        # Calculate AttrP
        AttrJ.clear()
        for j in range(0,len(J)):
            AttrJ.append(haversine(I[i,0], I[i,1], I[J[j][0],0], I[J[j][0],1]))
            
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