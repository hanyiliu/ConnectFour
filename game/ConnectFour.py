from tkinter import *
from functools import partial
import numpy as np
import Config
import os

size = [6,7] #rows, columns; i = row, j = column
rows = [] #2D array
buttons = []
board = np.zeros((6,7)) #2D array of board in numerical values #column, row
turn = 0 #0 = player 1, 1 = player 2
displayWinner = Label(text="Winner: ", justify="left", anchor="w")

#Data storage
player1Data = ([],[]) #list of board values
player2Data = ([],[])

def count_consecutive(arr, n):
    # pad a with False at both sides for edge cases when array starts or ends with n
    d = np.diff(np.concatenate(([False], arr == n, [False])).astype(int))
    # subtract indices when value changes from False to True from indices where value changes from True to False
    return np.flatnonzero(d == -1) - np.flatnonzero(d == 1)

def inputStatus(status):
    for i in range(np.size(buttons)):
        if(status):
            buttons[i].config(state=NORMAL)
        else:
            buttons[i].config(state=DISABLED)

def check(x,y):
    print("board: {}".format(board))
    vert = board[x] #add 0 zero, need 7
    hori = np.pad(board[:,y], (0, 1), 'constant') #add 1 zero
    diag = np.pad(np.diagonal(board,offset=(y-x)), (0, 7-np.size(np.diagonal(board,offset=(y-x)))), 'constant')
    fdiag = np.pad(np.diagonal(np.flip(board,axis=1),offset=(6-y-x)), (0, 7-np.size(np.diagonal(np.flip(board,axis=1),offset=(6-y-x)))), 'constant') #flipped diagonal

    v = np.array((vert,hori,diag,fdiag))
    print("v: {}".format(v))
    for i in range(np.size(v,0)):
        print(i)
        if np.any(count_consecutive(v[i],1) >= Config.mustConnect):
            print("Player 1 Wins.")
            displayWinner.config(text="Winner: Player 1")
            inputStatus(False)
            win(True)
        elif np.any(count_consecutive(v[i],2) >= Config.mustConnect):
            print("Player 2 Wins.")
            displayWinner.config(text="Winner: Player 2")
            inputStatus(False)
            win(False)

def move(column): #places piece in column
    global turn
    print("moving: {}".format(column))

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

            check(i,column);
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

def win(winner): #takes boolean, true for player 1 winning, false for player 2
    print(winner)
    #beginning data storage



    if winner: #player 1
        #saves input (board values)
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
        if os.stat(Config.player2InputDir).st_size == 0:
            np.savetxt(Config.player2InputDir, player2Data[0], fmt='%i')
        else:
            np.savetxt(Config.player2InputDir, np.append(np.genfromtxt(Config.player2InputDir), player2Data[0], 0), fmt='%i')

        #saves output (player choices)
        if os.stat(Config.player2OutputDir).st_size == 0:
            np.savetxt(Config.player2OutputDir, player2Data[1], fmt='%i')
        else:
            np.savetxt(Config.player2OutputDir, np.append(np.genfromtxt(Config.player2OutputDir), player2Data[1], 0), fmt='%i')


def main():


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

            e = Entry(relief=GROOVE)

            e.grid(row=i, column=j, sticky=NSEW, padx=5, pady=5, ipadx=1, ipady=1)

            e.insert(END, '')

            e.config(width=2)

            e.config(disabledbackground="white")


            e.config(state=DISABLED)

            cols.append(e)

        rows.append(cols)


    for j in range(size[1]): #create button to place pieces

        b = Button(command=partial(move, j))

        b.grid(row=7, column=j, padx=5, pady=5, ipadx=10, ipady=10)

        buttons.append(b)

    displayWinner.grid(row=8, columnspan=4, padx=20, pady=5, ipadx=10, ipady=10, sticky="w")

    r = Button(command=partial(reset))
    r.config(text="Reset")
    r.grid(row=8, column=7, padx=5, pady=5, ipadx=10, ipady=10)

    # rows[0][0].config(disabledbackground="purple");



    mainloop()

if __name__ == "__main__":
    main()
