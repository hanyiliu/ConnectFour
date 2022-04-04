from random import randrange
import time
import numpy as np
import statistics

from network.functions import hypothesis
from network.functions import reform
from game import ConnectFour
import Config

#Statistics
forceMoves = 0
wins = 0
wins1 = 0
wins2 = 0
averageCertainty = 0 #average of all guesses' certainty by the network. The lower the value, the more representative of simple guess and check
certainties = []

def simulate(rounds):
    global wins
    global wins1
    global wins2
    global forceMoves

    player1Theta = reform.reformTheta(np.genfromtxt(Config.player1ThetaDir))
    player2Theta = reform.reformTheta(np.genfromtxt(Config.player2ThetaDir))

    time.sleep(3)
    buttons = ConnectFour.getButtons()
    print("beginning simulation")
    iterations = 0

    if Config.eraseBeforeRound:
        if Config.trainingPlayer == 1:
            open(Config.player1InputDir, 'w').close()
            open(Config.player1OutputDir, 'w').close()
        elif Config.trainingPlayer == 2:
            open(Config.player2InputDir, 'w').close()
            open(Config.player2OutputDir, 'w').close()
        elif Config.trainingPlayer == 0:
            open(Config.player1InputDir, 'w').close()
            open(Config.player1OutputDir, 'w').close()
            open(Config.player2InputDir, 'w').close()
            open(Config.player2OutputDir, 'w').close()
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
                        forceMoves += 1
                        guess[move] = -guess[move]
                        move = np.argmax(guess)
                buttons[move].invoke()
                certainty = np.abs(guess[move])/np.sum(np.abs(guess)) #guess certainty divided by overall certainty
                certainties.append(certainty)
                print("guess certainty: {}".format(certainty*100))
            elif ConnectFour.getTurn() == 1:
                guess = hypothesis.hypothesis(ConnectFour.getBoard().flatten(), player2Theta)
                print("player 2, network guess: {}".format(np.argmax(guess)))

                move = np.argmax(guess)
                if Config.forceMove:
                    while not np.any(ConnectFour.getBoard()[:,move] == 0): #checks to see if there is available space in column
                        print("called")
                        forceMoves += 1
                        guess[move] = -guess[move]
                        move = np.argmax(guess)
                buttons[move].invoke()
                certainty = np.abs(guess[move])/np.sum(np.abs(guess)) #guess certainty divided by overall certainty
                certainties.append(certainty)
                print("guess certainty: {}".format(certainty*100))

                #buttons[randrange(7)].invoke()
                # while ConnectFour.getTurn() == 1: #waits for user input
                #     time.sleep(0.1)
            time.sleep(Config.waitTime)

        print("turn at end of round: {}".format(ConnectFour.getTurn())) #0 = player 2 won; 1 = player 1 won
        if Config.trainingPlayer == 0:
            if ConnectFour.getTurn() == 1:
                wins1 += 1
            else:
                wins2 += 1
        else:
            if ConnectFour.getTurn() == 1 and Config.trainingPlayer == 1:
                wins += 1
            elif ConnectFour.getTurn() == 0 and Config.trainingPlayer == 2:
                wins += 1

        ConnectFour.reset()

        averageCertainty = statistics.mean(certainties)
        print("finished iteration {}\n".format(iterations))
        iterations += 1

    print("finished\n")
    print("forcedMoves: {}".format(forceMoves))
    if Config.trainingPlayer == 0:
        print("player 1 wins: {} out of {} rounds".format(wins1, rounds))
        print("player 2 wins: {} out of {} rounds".format(wins2, rounds))
    else:
        print("wins: {} out of {} rounds".format(wins, rounds))
    print("averageCertainty: %.2f" % (averageCertainty*100))
    iterations += 1
