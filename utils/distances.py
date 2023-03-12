import numpy as np
import math

matrix = None

def haversine(lat1, lon1, lat2, lon2):
  # distance between latitudes and longitudes
  dLat = (lat2 - lat1) * math.pi / 180.0
  dLon = (lon2 - lon1) * math.pi / 180.0

  # convert to radians
  lat1 = (lat1) * math.pi / 180.0
  lat2 = (lat2) * math.pi / 180.0

  # apply formulae
  a = (pow(math.sin(dLat / 2), 2) +
        pow(math.sin(dLon / 2), 2) *
        math.cos(lat1) * math.cos(lat2))
  rad = 6371
  c = 2 * math.asin(math.sqrt(a))
  return rad * c

# maps distances into an array that represents a triangular matrix
def buildTriangleMatrix(I):
  idxi = 0
  global matrix
  matrix = np.zeros(round((len(I)*(len(I)-1))/2))
  for i in I:
    idxj = 0
    for j in I[:idxi]:
      matrix[getTriangleIndex(idxi, idxj)] = haversine(i[0], i[1], j[0], j[1])
      idxj += 1
    idxi += 1
  return matrix

def getTriangleIndex(i, j): 
  if j > i: i, j = j, i
  return int((i * (i-1))/2+j)

def dist(i, j, input):
  if type(input[0]) == np.ndarray:
    return haversine(input[i][0], input[i][1], input[j][0], input[j][1])
  else: 
    return 1 if i == j else input[getTriangleIndex(i, j)]