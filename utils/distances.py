import numpy as np
import os
import math
import time
from os.path import exists

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
def buildTriangleMatrix(I: 'np.ndarray[np.ndarray[float]]'):
  global matrix
  if exists(f'distances/{len(I)}_points.dat'):
    file = open(f'distances/{len(I)}_points.dat', 'rb')
    matrix = np.frombuffer(file.read())
  else:
    startTime = time.time()
    idxi = 0
    matrix = np.zeros(round((len(I)*(len(I)-1))/2))
    for i in I:
      idxj = 0
      for j in I[:idxi]:
        matrix[getTriangleIndex(idxi, idxj)] = haversine(i[0], i[1], j[0], j[1])
        idxj += 1
      idxi += 1
    print(f'Distance matrix was calculated in {round(time.time() - startTime, 4)} seconds')
    # write the matrix to file
    os.makedirs('./distances', exist_ok=True)
    open(f'./distances/{len(I)}_points.dat', 'wb').write(matrix.tobytes());
  return matrix

def assignNoDistances(I: 'np.ndarray[np.ndarray[float]]'):
  global matrix
  matrix = I
  return I

def getTriangleIndex(i, j): 
  if j > i: i, j = j, i
  return int((i * (i-1))/2+j)

def dist(i: int, j: int) -> float:
  if matrix is None: raise ValueError("Distance matrix was not initiated")
  if i == j: return 0
  if type(matrix[0]) == np.ndarray:
    return haversine(matrix[int(i)][0], matrix[int(i)][1], matrix[int(j)][0], matrix[int(j)][1])
  else: 
    return matrix[getTriangleIndex(i, j)]