import numpy as np
import Config

def sigmoid(z):
    #print(-z)
    return 1.0 / (1.0 + np.exp(-z.astype(np.longdouble)))

def hypothesis(x, t, computingGradient = False, printData = False):

    print("Starting hypothesis")

    aList = []
    zList = []

    x = np.insert(x, 0, 1, axis=0) #Add bias unit to input

    z = np.dot(t[0], x)
    zList.append(z)
    a = sigmoid(z)
    aList.append(a)
    a = np.insert(a, 0, 1, axis=0) #Add bias unit to a

    z = np.dot(t[1], a)
    zList.append(z)
    a = sigmoid(z)
    aList.append(a)
    a = np.insert(a, 0, 1, axis=0) #Add bias unit to a

    #TODO: put this into a for loop later on

    h = np.dot(t[2], a)
    zList.append(h)

    h = sigmoid(h)
    aList.append(h)

    if computingGradient:
        return h, aList, zList
    else:
        return h
