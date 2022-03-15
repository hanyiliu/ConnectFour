import numpy as np
import Config
from network.functions import hypothesis

def sigmoid(z):
    #print(-z)
    return 1.0 / (1.0 + np.exp(-z.astype(np.longdouble)))
def sigmoidGradient(z):
    return sigmoid(z)*(1-sigmoid(z));

def computeGradient(x, t, y): #For only one input and output right now
    h,a,z = hypothesis.hypothesis(x,t, computingGradient=True) #Step 1

    deltaList = []

    #This goes backwards (back-propagation)
    delta = a[-1]-y #for output units
    deltaList.insert(0, delta) #delta 4


    z[1] = np.insert(z[1], 0, 0, axis=0) #add 0 to account for bias unit
    delta = np.dot(t[2].T,delta)*sigmoidGradient(z[1])
    delta = np.delete(delta, 0) #remove bias unit's delta
    deltaList.insert(0, delta) #delta 3

    z[0] = np.insert(z[0], 0, 0, axis=0) #add 0 to account for bias unit
    delta = np.dot(t[1].T,delta)*sigmoidGradient(z[0])
    delta = np.delete(delta, 0) #remove bias unit's delta
    deltaList.insert(0, delta) #delta 2 (does not need delta 1)

    print(deltaList)
    print(np.shape(deltaList[2]))
    print(np.shape(deltaList[1]))
    print(np.shape(deltaList[0]))
