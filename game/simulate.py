from random import randrange
import time
import numpy as np
import statistics
import os

from network.functions import hypothesis
from network.functions import reform
from game import ConnectFour
from game import manualBot
import Config

#Statistics
forceMoves = 0
wins = 0
wins1 = 0
wins2 = 0
averageCertainty = 0 #average of all guesses' certainty by the network. The lower the value, the more representative of simple guess and check
certainties = []

def simulate(rounds, train):
    global wins
    global wins1
    global wins2
    global forceMoves

    for i in range(0, Config.loopIterations):
        if not Config.randomTheta:
            try:
                player1Theta = reform.reformTheta(np.genfromtxt(Config.player1ThetaDir))
                player2Theta = reform.reformTheta(np.genfromtxt(Config.player2ThetaDir))
            except UserWarning:
                print("theta file empty")

        time.sleep(3)
        buttons = ConnectFour.getButtons()
        print("beginning simulation")

        iterations = 0

        if Config.eraseBeforeRound:
            if Config.trainingPlayer == 1:
                open(Config.player1InputDir, 'w').close()
                open(Config.player1OutputDir, 'w').close()
                open(Config.player1EpsilonDir, 'w').close()
            elif Config.trainingPlayer == 2:
                open(Config.player2InputDir, 'w').close()
                open(Config.player2OutputDir, 'w').close()
                open(Config.player2EpsilonDir, 'w').close()
            elif Config.trainingPlayer == 0:
                open(Config.player1InputDir, 'w').close()
                open(Config.player1OutputDir, 'w').close()
                open(Config.player1EpsilonDir, 'w').close()
                open(Config.player2InputDir, 'w').close()
                open(Config.player2OutputDir, 'w').close()
                open(Config.player2EpsilonDir, 'w').close()
        while iterations < rounds:
            print("round: {}".format(iterations))
            network1 = False
            network2 = False


            while not ConnectFour.getEndStatus():
                if not Config.randomGuess:
                    if os.stat(Config.player1ThetaDir).st_size == 0 or os.stat(Config.player2ThetaDir).st_size == 0:
                        print("theta files not present. stopping simulation")
                        return
                if ConnectFour.getTurn() == 0:
                    while ConnectFour.getTurn() == 2: #waits for user input
                         time.sleep(0.1)
                    # if Config.randomGuess:
                    #     buttons[randrange(7)].invoke()
                    # elif Config.mutation:
                    #     if Config.mutationChance*100 >= randrange(100):
                    #         buttons[randrange(7)].invoke()
                    #     else:
                    #         guess = hypothesis.hypothesis(player1Theta, ConnectFour.getBoard().flatten())
                    #         if Config.printLogs:
                    #             print("player 1, network guess: {}".format(np.argmax(guess)))
                    #
                    #         move = np.argmax(guess)
                    #         if Config.forceMove:
                    #             fullCheck = 0
                    #             while not np.any(ConnectFour.getBoard()[:,move] == 0): #checks to see if there is available space in column
                    #                 if Config.printLogs:
                    #                     print("called")
                    #                 forceMoves += 1
                    #                 fullCheck += 1
                    #                 if fullCheck > 10:
                    #                     ConnectFour.reset()
                    #                 guess[move] = -guess[move]
                    #                 move = np.argmax(guess)
                    #         buttons[move].invoke()
                    #         certainty = np.abs(guess[move])/np.sum(np.abs(guess)) #guess certainty divided by overall certainty
                    #         certainties.append(certainty)
                    #         if Config.printLogs:
                    #             print("guess certainty: {}".format(certainty*100))
                    # else:
                    #     if Config.useNetwork == 2:
                    #         buttons[randrange(7)].invoke()
                    #     else:
                    #         guess = hypothesis.hypothesis(player1Theta, ConnectFour.getBoard().flatten())
                    #         if Config.printLogs:
                    #             print("player 1, network guess: {}".format(np.argmax(guess)))
                    #
                    #         move = np.argmax(guess)
                    #         if Config.forceMove:
                    #             while not np.any(ConnectFour.getBoard()[:,move] == 0): #checks to see if there is available space in column
                    #                 print("called")
                    #                 forceMoves += 1
                    #                 guess[move] = -guess[move]
                    #                 move = np.argmax(guess)
                    #         buttons[move].invoke()
                    #         certainty = np.abs(guess[move])/np.sum(np.abs(guess)) #guess certainty divided by overall certainty
                    #         certainties.append(certainty)
                    #         if Config.printLogs:
                    #             print("guess certainty: {}".format(certainty*100))
                    #
                    #         # while ConnectFour.getTurn() == 1: #waits for user input
                    #         #      time.sleep(0.1)
                elif ConnectFour.getTurn() == 1:

                    # while ConnectFour.getTurn() == 1: #waits for user input
                    #      time.sleep(0.1)


                    if Config.randomGuess:
                        buttons[randrange(7)].invoke()
                    elif Config.useManualBot:
                        scores = manualBot.hypothesis(ConnectFour.getBoard())
                        guess = np.random.choice(np.flatnonzero(scores == scores.max()))
                        buttons[guess].invoke()
                    elif Config.mutation:

                        # while ConnectFour.getTurn() == 1: #waits for user input
                        #      time.sleep(0.1)
                        if Config.mutationChance*100 >= randrange(100):
                            buttons[randrange(7)].invoke()
                        else:
                            guess = hypothesis.hypothesis(player1Theta, ConnectFour.getBoard().flatten())
                            if Config.printLogs:
                                print("player 2, network guess: {}".format(np.argmax(guess)))

                            move = np.argmax(guess)
                            if Config.forceMove:
                                forceCheck = 0
                                while not np.any(ConnectFour.getBoard()[:,move] == 0): #checks to see if there is available space in column
                                    if Config.printLogs:
                                        print("called")
                                    forceMoves += 1
                                    fullCheck += 1
                                    if fullCheck > 10:
                                        ConnectFour.reset()
                                    guess[move] = -guess[move]
                                    move = np.argmax(guess)
                            buttons[move].invoke()
                            certainty = np.abs(guess[move])/np.sum(np.abs(guess)) #guess certainty divided by overall certainty
                            certainties.append(certainty)
                            if Config.printLogs:
                                print("guess certainty: {}".format(certainty*100))
                    else:
                        if Config.useNetwork == 1 or Config.randomGuess:
                            buttons[randrange(7)].invoke()
                        else:
                            guess = hypothesis.hypothesis(player2Theta, ConnectFour.getBoard().flatten())
                            if Config.printLogs:
                                print("player 2, network guess: {}".format(np.argmax(guess)))

                            move = np.argmax(guess)
                            if Config.forceMove:
                                while not np.any(ConnectFour.getBoard()[:,move] == 0): #checks to see if there is available space in column
                                    if Config.printLogs:
                                        print("called")
                                    forceMoves += 1
                                    guess[move] = -guess[move]
                                    move = np.argmax(guess)
                            buttons[move].invoke()
                            certainty = np.abs(guess[move])/np.sum(np.abs(guess)) #guess certainty divided by overall certainty
                            certainties.append(certainty)
                            if Config.printLogs:
                                print("guess certainty: {}".format(certainty*100))


                            while ConnectFour.getTurn() == 1: #waits for user input
                                 time.sleep(0.1)
                time.sleep(Config.waitTime)

            if Config.printLogs:
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


            if Config.printLogs:
                print("finished iteration {}\n".format(iterations))
            iterations += 1

        print("finished\n")
        print("forcedMoves: {}".format(forceMoves))
        if Config.trainingPlayer == 0:
            print("player 1 wins: {} out of {} rounds".format(wins1, rounds))
            print("player 2 wins: {} out of {} rounds".format(wins2, rounds))
        else:
            print("wins: {} out of {} rounds".format(wins, rounds))

        if not Config.randomGuess:
            averageCertainty = statistics.mean(certainties)
            print("averageCertainty: %.2f" % (averageCertainty*100))

        wins = 0
        wins1 = 0
        wins2 = 0
        forceMoves = 0
        train()
