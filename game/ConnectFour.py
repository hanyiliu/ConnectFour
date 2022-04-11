from tkinter import *
from functools import partial
import numpy as np
import Config
import os

from game import check


size = [6,7] #rows, columns; i = row, j = column
rows = [] #2D array
buttons = []
board = np.zeros((6,7)) #2D array of board in numerical values #column, row
turn = 0 #0 = player 1, 1 = player 2
endStatus = False
displayWinner = Label(text="Winner: ", justify="left", anchor="w")

#Data storage
player1Data = ([],[]) #list of board values, choice
player2Data = ([],[]) #list of board values, choice

def getButtons():
    return buttons

def getBoard():
    return board

def getTurn():
    return turn

def getEndStatus():
    return endStatus
def setEndStatus(newStatus):
    global endStatus
    endStatus = newStatus

def quit():
    global root
    root.destroy()

def inputStatus(status):
    for i in range(np.size(buttons)):
        if(status):
            buttons[i].config(state=NORMAL)
        else:
            buttons[i].config(state=DISABLED)


def move(column): #places piece in column
    global turn

    for i in range(size[0]-1,-1,-1): #reversed iteration because piece goes to bottom, not top lol
        if(rows[i][column].cget("disabledbackground") == "white"):
            if(turn == 0):
                #storing data
                player1Data[0].append(board.flatten())
                player1Data[1].append(column)

                #updating board
                rows[i][column].config(disabledbackground="red")
                board[i][column] = Config.playerValue
                turn = 1



            else:
                #storing data
                player2Data[0].append(board.flatten())
                player2Data[1].append(column)

                #updating board
                rows[i][column].config(disabledbackground="yellow")
                board[i][column] = Config.opponentValue
                turn = 0

            state = check.check(board,i,column)
            if state == 1:
                print("Player 1 Wins.")
                displayWinner.config(text="Winner: Player 1")
                inputStatus(False)
                win(True)
            elif state == 2:
                print("Player 2 Wins.")
                displayWinner.config(text="Winner: Player 2")
                inputStatus(False)
                win(False)
            return

def reset():

    global board
    global turn
    global displayWinner

    for i in range(size[0]): #create each point on board
        for j in range(size[1]):
            rows[i][j].config(disabledbackground="white")

    board = np.zeros((6,7)) #2D array of board in numerical values #column, row
    turn = 0 #0 = player 1, 1 = player 2
    displayWinner.config(text="Winner: ")
    inputStatus(True)
    setEndStatus(False)

def win(winner): #takes boolean, true for player 1 winning, false for player 2
    global endStatus
    global player1Data
    global player2Data
    endStatus = True

    #beginning data storage


    if winner: #player 1
        #saves input (board values)
        epsilon = 1
        epsilonList = np.zeros((0,0))
        for i in range(0,np.shape(player1Data[0])[0]):
            epsilonList = np.append(epsilonList,epsilon)
            epsilon = epsilon * Config.epsilonRate
        epsilonList = epsilonList[::-1]
        #saves epsilons
        if os.stat(Config.player1EpsilonDir).st_size == 0: #if empty, write file. Otherwise, append to existing data
            np.savetxt(Config.player1EpsilonDir, epsilonList)
        else:
            np.savetxt(Config.player1EpsilonDir, np.append(np.genfromtxt(Config.player1EpsilonDir), epsilonList, 0))

        if os.stat(Config.player1InputDir).st_size == 0: #if empty, write file. Otherwise, append to existing data
            np.savetxt(Config.player1InputDir, player1Data[0], fmt='%i')
        else:
            np.savetxt(Config.player1InputDir, np.append(np.genfromtxt(Config.player1InputDir), player1Data[0], 0), fmt='%i')

        #saves output (player choices)
        if os.stat(Config.player1OutputDir).st_size == 0:
            np.savetxt(Config.player1OutputDir, player1Data[1], fmt='%i')
        else:
            np.savetxt(Config.player1OutputDir, np.append(np.genfromtxt(Config.player1OutputDir), player1Data[1], 0), fmt='%i')
    else: #player 2
        #saves input (board values)
        epsilon = 1
        epsilonList = np.zeros((0,0))
        for i in range(0,np.shape(player2Data[0])[0]):
            epsilonList = np.append(epsilonList,epsilon)
            epsilon = epsilon * Config.epsilonRate
        epsilonList = epsilonList[::-1]
        #saves epsilons
        if os.stat(Config.player2EpsilonDir).st_size == 0: #if empty, write file. Otherwise, append to existing data
            np.savetxt(Config.player2EpsilonDir, epsilonList)
        else:
            np.savetxt(Config.player2EpsilonDir, np.append(np.genfromtxt(Config.player2EpsilonDir), epsilonList, 0))

        if os.stat(Config.player2InputDir).st_size == 0:
            np.savetxt(Config.player2InputDir, player2Data[0], fmt='%i')
        else:
            np.savetxt(Config.player2InputDir, np.append(np.genfromtxt(Config.player2InputDir), player2Data[0], 0), fmt='%i')

        #saves output (player choices)
        if os.stat(Config.player2OutputDir).st_size == 0:
            np.savetxt(Config.player2OutputDir, player2Data[1], fmt='%i')
        else:
            np.savetxt(Config.player2OutputDir, np.append(np.genfromtxt(Config.player2OutputDir), player2Data[1], 0), fmt='%i')


    player1Data = ([],[])
    player2Data = ([],[])
def main():

    global root
    global displayWinner
    root = Tk()

    #create files for data storage (if not present)
    try:
        open(Config.player1InputDir, 'x')
    except FileExistsError:
        print("Player 1 input file exists.")

    try:
        open(Config.player1OutputDir, 'x')
    except FileExistsError:
        print("Player 1 output file exists.")

    try:
        open(Config.player2InputDir, 'x')
    except FileExistsError:
        print("Player 2 input file exists.")

    try:
        open(Config.player2OutputDir, 'x')
    except FileExistsError:
        print("Player 2 output file exists.")

    for i in range(size[0]): #create each point on board
        cols = []

        for j in range(size[1]):

            e = Entry(root,relief=GROOVE)

            e.grid(row=i, column=j, sticky=NSEW, padx=5, pady=5, ipadx=1, ipady=1)

            e.insert(END, '')

            e.config(width=2)

            e.config(disabledbackground="white")


            e.config(state=DISABLED)

            cols.append(e)

        rows.append(cols)


    for j in range(size[1]): #create button to place pieces

        b = Button(root,command=partial(move, j))

        b.grid(row=7, column=j, padx=5, pady=5, ipadx=10, ipady=10)

        buttons.append(b)

    displayWinner.grid(row=8, columnspan=4, padx=20, pady=5, ipadx=10, ipady=10, sticky="w")

    r = Button(root,command=partial(reset))
    r.config(text="Reset")
    r.grid(row=8, column=7, padx=5, pady=5, ipadx=10, ipady=10)

    # rows[0][0].config(disabledbackground="purple");
    displayWinner = Label(root,text="Winner: ", justify="left", anchor="w")
    #automated loops
    root.mainloop()




# if __name__ == "__main__":
#     main()
