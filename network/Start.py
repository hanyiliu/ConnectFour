import numpy as np

from functions import cost

y = np.array((0,1,1,0))
h = np.array((0.999,0.001,0.001,0.999))

cost = cost.cost(h,y)

print(cost)
