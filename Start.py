import numpy as np
import Config
import threading
import os

from network.functions import train

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
    train.train(x,y,0)
    print("finished training player 1")
elif Config.trainingPlayer == 2:
    x = np.genfromtxt(Config.player2InputDir)
    y = toBinary(np.genfromtxt(Config.player2OutputDir))
    train.train(x,y,1)
    print("finished training player 2")
elif Config.trainingPlayer == 0: #training both

    x = np.genfromtxt(Config.player1InputDir)
    y = toBinary(np.genfromtxt(Config.player1OutputDir))
    train.train(x,y,0)
    print("finished training player 1")

    x = np.genfromtxt(Config.player2InputDir)
    y = toBinary(np.genfromtxt(Config.player2OutputDir))
    train.train(x,y,1)
    print("finished training player 2")

print("data shapes:")
print("x: {}".format(np.shape(x)))
print("y: {}".format(np.shape(y)))
