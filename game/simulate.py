from random import randrange
import time
import numpy as np

from network.functions import hypothesis
from game import ConnectFour
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


def simulate(rounds):

    player1Theta = reformTheta(np.genfromtxt(Config.player1ThetaDir))
    player2Theta = reformTheta(np.genfromtxt(Config.player2ThetaDir))

    time.sleep(3)
    buttons = ConnectFour.getButtons()
    print("beginning simulation")
    iterations = 0

    while iterations < rounds:
        print("round: {}".format(iterations))
        while not ConnectFour.getEndStatus():
            if ConnectFour.getTurn() == 0:
                guess = hypothesis.hypothesis(ConnectFour.getBoard().flatten(), player1Theta)
                print("player 1, network guess: {}".format(np.argmax(guess)))

                move = np.argmax(guess)
                if Config.forceMove:
                    while not np.any(ConnectFour.getBoard()[:,move] == 0): #checks to see if there is available space in column
                        print("called")
                        guess[move] = 0
                        move = np.argmax(guess)
                buttons[move].invoke()
            elif ConnectFour.getTurn() == 1:
                # guess = hypothesis.hypothesis(ConnectFour.getBoard().flatten(), player2Theta)
                # print("player 2, network guess: {}".format(np.argmax(guess)))
                #
                # move = np.argmax(guess)
                # if Config.forceMove:
                #     while not np.any(ConnectFour.getBoard()[:,move] == 0): #checks to see if there is available space in column
                #         print("called")
                #         guess[move] = 0
                #         move = np.argmax(guess)
                buttons[randrange(7)].invoke()
            time.sleep(Config.waitTime)
        ConnectFour.reset()
        print("finished round {}".format(iterations))
        iterations += 1
        
