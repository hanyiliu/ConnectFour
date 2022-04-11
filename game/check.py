import numpy as np
import Config

def count_consecutive(arr, n):
    # pad a with False at both sides for edge cases when array starts or ends with n
    d = np.diff(np.concatenate(([False], arr == n, [False])).astype(int))
    # subtract indices when value changes from False to True from indices where value changes from True to False
    return np.flatnonzero(d == -1) - np.flatnonzero(d == 1)

def check(board,x,y): #returns reward,winstatus (0,1,2)
    vert = board[x] #add 0 zero, need 7
    hori = np.pad(board[:,y], (0, 1), 'constant') #add 1 zero
    diag = np.pad(np.diagonal(board,offset=(y-x)), (0, 7-np.size(np.diagonal(board,offset=(y-x)))), 'constant')
    fdiag = np.pad(np.diagonal(np.flip(board,axis=1),offset=(6-y-x)), (0, 7-np.size(np.diagonal(np.flip(board,axis=1),offset=(6-y-x)))), 'constant') #flipped diagonal
    v = np.array((vert,hori,diag,fdiag))
    for i in range(np.size(v,0)):
        if np.any(count_consecutive(v[i],1) >= Config.mustConnect):
            return 1

        elif np.any(count_consecutive(v[i],2) >= Config.mustConnect):
            return 2

    return 0

def check_all(board,player,connect_four_score=4): #player = 1,2.
    #Checks the amount of marbles connected if player places marble in each column

    score = np.zeros(7)



    for i in range(0,7):
        while not np.any(board[:,i] == 0):
            if i == 6:
                return score
            i += 1
        x = np.argwhere(board[:,i] == 0).max() #gets last occurance of 0
        y = i
        future_board = np.copy(board)
        future_board[x,y] = player



        vert = future_board[x] #add 0 zero, need 7
        hori = np.pad(future_board[:,y], (0, 1), 'constant') #add 1 zero
        diag = np.pad(np.diagonal(future_board,offset=(y-x)), (0, 7-np.size(np.diagonal(future_board,offset=(y-x)))), 'constant')
        fdiag = np.pad(np.diagonal(np.flip(future_board,axis=1),offset=(6-y-x)), (0, 7-np.size(np.diagonal(np.flip(future_board,axis=1),offset=(6-y-x)))), 'constant') #flipped diagonal

        v = [vert,hori,diag,fdiag]
        for j in range(len(v)): #Config.mustConnect = 4
            consecutives = count_consecutive(v[j],player)
            if np.any(consecutives >= Config.mustConnect):
                score[i] = connect_four_score
                break #no need to check for more, this is maximum score
            elif np.any(consecutives > score[i]):
                score[i] = np.max(consecutives)

    return score
