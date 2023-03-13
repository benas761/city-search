from utils.distances import dist

def binary(potentialFacilities, args):
    
    AttrJ = []          # attractiveness of all preexisting facilities
    AttrX = []          # attractiveness of all new facilities
    utility = 0         # utility of the new facilties
    totalDemand = 0     # total demand of the whole population
    
    for i in range(0, len(args['population'])):
        totalDemand = totalDemand + args['population'][i]
        
        # Calculate AttrP
        AttrJ.clear()
        for j in args['competitors']:
            AttrJ.append(dist(i, j, args['distance']))
            
        # Calculate AttrX
        AttrX.clear()
        for j in potentialFacilities:
            AttrX.append(dist(i, j, args['distance']))
        
        # If the best of AttrX is better than the best of AttrJ
        if (min(AttrX) < min(AttrJ)):
            utility = utility + args['population'][i]
        
        # If the best of Attr is equal to the best of AttrJ
        elif (min(AttrX) == min(AttrJ)):
            utility = utility + args['population'][i]/3

    return utility/totalDemand*100