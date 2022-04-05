import numpy as np
import Config

from network.functions import cost
from network.functions import hypothesis
from network.functions import computeGradient
from network.functions import reform

def train(x, y, epsilon, player): #player = 0,1
    a = 0.001 #alpha value
    m = np.shape(x)[0]

    #[5,2]
    if Config.randomTheta:
        t = np.random.uniform(-1, 1, (Config.networksize[1]+1,Config.networksize[0],Config.networksize[0]+1)) #[# of layers, # of neurons, # of neurons + 1 to account for bias unit]

        print(np.shape(t))
        thetaList = []
        for i in range(0, np.shape(t)[0]):
            if i == 0: #Fix first layer to account for input units
                thetaList.append(t[0,:,0:Config.input+1])
            elif i == np.shape(t)[0]-1: #Fix last layer to account for output units
                thetaList.append(t[-1,0:Config.output])
            else:
                thetaList.append(t[i])

        t = thetaList
    else:
        if player == 0:
            t = reform.reformTheta(np.genfromtxt(Config.player1ThetaDir))
        if player == 1:
            t = reform.reformTheta(np.genfromtxt(Config.player1ThetaDir))
        else:
            print("ok how are u actually here now")
    costs = []
    c = 0 #cost
    g = [np.zeros(np.shape(t[0])), np.zeros(np.shape(t[1])), np.zeros(np.shape(t[2]))] #gradient
    for j in range(0,Config.iterations):
        for i in range(0, np.shape(x)[0]):
            hypothesis0 = hypothesis.hypothesis(x[i], t)
            gradient = computeGradient.computeGradient(x[i], t, y[i])


            cost0 = cost.cost(hypothesis0,y[i])

            #either place epsilon here or place at t - g
            g[0] = g[0] + epsilon[i]*gradient[0]
            g[1] = g[1] + epsilon[i]*gradient[1]
            g[2] = g[2] + epsilon[i]*gradient[2]

            costs.append(cost0)
            c = cost0

        t[0] = t[0] - g[0]/m
        t[1] = t[1] - g[1]/m
        t[2] = t[2] - g[2]/m
        g = [np.zeros(np.shape(t[0])), np.zeros(np.shape(t[1])), np.zeros(np.shape(t[2]))]
        print("finished iteration {} of {}. cost: {}%".format(j+1, Config.iterations, c))

    print("finished, saving thetas")
    print(np.shape(t[0]))
    print(np.shape(t[1]))
    print(np.shape(t[2]))
    flatThetas = np.concatenate([t[0].flatten(),t[1].flatten(),t[2].flatten()])
    if player == 0: #Overwrites current theta values
        np.savetxt(Config.player1ThetaDir, flatThetas) #Overwrites current theta values. TODO: fix numpy conversion
    elif player == 1:
        np.savetxt(Config.player2ThetaDir, flatThetas)
    else:
        print("how tf did you even make it to this point")

    print("overall cost improvement: {}%".format(100*abs(costs[0]-costs[-1])/((costs[0]+costs[-1])/2)))
