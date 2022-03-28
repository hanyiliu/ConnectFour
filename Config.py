#game
playerValue = 1
opponentValue = 2
mustConnect = 4
training = False #Set to true if training datasets
simulate = True #Set to true if simulating datasets (training must be True too)
autoReset = False #Automatically reset upon winner

#Training
networksize = (42,2) #neurons per layer, number of layers #TODO: cannot change layers, must fix
#TODO: the number of neurons per layer currently has to be greater than the number of input and output units; this can be fixed but im lazy

input = 42 #number of input units
output = 7 #number of output units

lamb = 1
alpha = 0.001 #alpha value
iterations = 5 #for actually training thetas
trainingPlayer = 1 #which player is currently being trained

#Data
gameIterations = 10 #for creating dataset

player1InputDir = "data/player1/input.txt" #Red guy
player1OutputDir = "data/player1/output.txt"
player1ThetaDir = "data/player1/theta.txt"

player2InputDir = "data/player2/input.txt" #Yellow guy
player2OutputDir = "data/player2/output.txt"
player2ThetaDir = "data/player2/theta.txt"
