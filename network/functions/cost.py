import numpy as np

def cost(h,y): #where h and y are same size and numpy arrays, NOT REGULARIZED
    m = np.size(y)

    cost = (-1/m) * (y*np.log(h) + (1-y)*np.log(1-h))
    
    return np.sum(cost)
