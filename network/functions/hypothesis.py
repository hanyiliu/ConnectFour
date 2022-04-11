import numpy as np
import Config

from network.functions import reform

def sigmoid(z):
    #print(-z)
    return 1.0 / (1.0 + np.exp(-z.astype(np.longdouble)))

def hypothesis(t, x, placeholder=0, computingGradient = False, printData = False):
    print(type(t))
    if isinstance(t,np.ndarray):
        print(np.shape(t))
    if isinstance(t,np.ndarray) and np.shape(t)[0] == 1:
        print("yes")
        t = reform.reformTheta(t) #for bfgs, whose theta input is flattened


    print("hypothesis shapes:")
    #print("theta: {}".format(np.shape(t)))
    print("x: {}".format(np.shape(x)))

    aList = []
    zList = []

    x = np.insert(x, 0, 1, axis=0) #Add bias unit to input
    aList.append(x) #a0


    z = np.dot(t[0], x)
    zList.append(z) #z0
    a = sigmoid(z)
    a = np.insert(a, 0, 1, axis=0) #Add bias unit to a
    aList.append(a) #a1

    z = np.dot(t[1], a)
    zList.append(z) #z1
    a = sigmoid(z)
    a = np.insert(a, 0, 1, axis=0) #Add bias unit to a
    aList.append(a) #a2

    #TODO: put this into a for loop later on

    h = np.dot(t[2], a)
    zList.append(h) #z2

    h = sigmoid(h)
    aList.append(h) #a3

    if computingGradient:
        return h, aList, zList
    else:
        return h
