import numpy as np
import Config
import threading
import os

from network.functions import cost
from network.functions import hypothesis
from network.functions import computeGradient

from game import ConnectFour
from game import simulate

##################################################################
#       Plan of attack:
#           - run game i times
#           - after i iterations, feed data into network
#           - train both players, but with differing values
#           - after training completes, repeat overall loop
#       - then itll all magically work right
#       TODO: include randomization if needed
##################################################################

def toBinary(y):
    if np.size(np.shape(np.array([y]))) == 1 or np.shape(np.array([y]))[0] == 1:
        #print("yes it does")
        try:
            yZeros = np.zeros((np.shape(y)[0], Config.output))
        except IndexError:
            yZeros = np.zeros((1, Config.output))
        if np.size(np.shape(y)) == 1:
            yZeros[np.arange(np.size(y)),y.astype(int)-1] = 1
            y = yZeros

    return y

if Config.training:
    ConnectFour.main()
if Config.simulate:
    simulationThread = threading.Thread(target=simulate.simulate, args=(Config.gameIterations,))
    simulationThread.start()
    ConnectFour.main() #Starts the game ui
np.set_printoptions(edgeitems=30, linewidth=100000)

#XOR logic gate data values:
# x = np.array(([0,0],
#              [0,1],
#              [1,0],
#              [1,1])) #0,1,1,0
#
# y = np.array(([1,0],
#               [0,1],
#               [0,1],
#               [1,0])) #[False,True]

try:
    open(Config.player1ThetaDir, 'x')
except FileExistsError:
    print("Player 1 theta file exists.")

try:
    open(Config.player2ThetaDir, 'x')
except FileExistsError:
    print("Player 2 theta file exists.")

if Config.trainingPlayer == 1: #get training data
    x = np.genfromtxt(Config.player1InputDir)
    y = toBinary(np.genfromtxt(Config.player1OutputDir))
    print("Training  player 1")
elif Config.trainingPlayer == 2:
    x = np.genfromtxt(Config.player2InputDir)
    y = toBinary(np.genfromtxt(Config.player2OutputDir))
    print("Training  player 2")
else:
    print("wtf are you doing")

print("data shapes:")
print("x: {}".format(np.shape(x)))
print("y: {}".format(np.shape(y)))


a = 0.001 #alpha value
m = np.shape(x)[0]

#[5,2]
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
costs = []
c = 0 #cost
g = [np.zeros(np.shape(t[0])), np.zeros(np.shape(t[1])), np.zeros(np.shape(t[2]))] #gradient
for j in range(0,Config.iterations):
    for i in range(0, np.shape(x)[0]):
        hypothesis0 = hypothesis.hypothesis(x[i], t)
        gradient = computeGradient.computeGradient(x[i], t, y[i])


        cost0 = cost.cost(hypothesis0,y[i])


        g[0] = g[0] + gradient[0]
        g[1] = g[1] + gradient[1]
        g[2] = g[2] + gradient[2]

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
if Config.trainingPlayer == 1: #Overwrites current theta values
    np.savetxt(Config.player1ThetaDir, flatThetas) #Overwrites current theta values. TODO: fix numpy conversion
elif Config.trainingPlayer == 2:
    np.savetxt(Config.player2ThetaDir, flatThetas)
else:
    print("how tf did you even make it to this point")

print("overall cost improvement: {}%".format(100*abs(costs[0]-costs[-1])/((costs[0]+costs[-1])/2)))
