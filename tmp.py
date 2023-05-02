import numpy as np
import matplotlib.pyplot as plt
filepath = 'data/demands_LT_12395.dat'
file = np.loadtxt(filepath)
x = [f[0] for f in file]
y = [f[1] for f in file]
plt.axis([50, 60, 20, 30])
plt.scatter(x, y)
plt.title('Lietuvos miestai')
plt.show()