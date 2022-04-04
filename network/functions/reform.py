import numpy as np
import Config

def reformTheta(t): #takes flattened thetas
    thetaList = []
    print("Reforming theta")
    for i in range(0,Config.networksize[1]+1):


        if i == 0: #input layer
            numberOfThetas = Config.input*(Config.networksize[0]+1)
            theta = np.reshape(t[0:numberOfThetas], (Config.input,Config.networksize[0]+1))
        if i == Config.networksize[1]: #output layer
            numberOfThetas = Config.output*(Config.networksize[0]+1) #should be the same value
            theta = np.reshape(t,(Config.output,Config.networksize[0]+1))
        else: #hidden layers
            numberOfThetas = Config.networksize[0]*(Config.networksize[0]+1)
            theta = np.reshape(t[0:numberOfThetas], (Config.networksize[0],Config.networksize[0]+1))

        t = t[numberOfThetas:]
        thetaList.append(theta)

    return thetaList
