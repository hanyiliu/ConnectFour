#game
playerValue = 1
opponentValue = 2
mustConnect = 4
training = False #Set to true if training datasets
simulate = True #Set to true if simulating datasets (training must be True too)
autoReset = False #Automatically reset upon winner

#simulation
eraseBeforeRound = True #Erase data before every full simulation (only erases player being trained's data)
forceMove = True #Set to true if manually forcing network to go to other options when first option is unavailable (column already filled)
waitTime = 0.05 #How long to wait inbetween moves (s)
randomGuess = False #Randomly guess
useNetwork = 1 #0 for both, 1 for player 1, 2 for player 2

mutation = True #Random actions when using network
mutationChance = 0.5
#Training
networksize = (42,2) #neurons per layer, number of layers #TODO: cannot change layers, must fix
#TODO: the number of neurons per layer currently has to be greater than the number of input and output units; this can be fixed but im lazy

input = 42 #number of input units
output = 7 #number of output units

lamb = 1
alpha = 0.001 #alpha value
epsilonRate = 0.9 #how much to apply to episode prior to winning
iterations = 5 #for actually training thetas
trainingPlayer = 0 #which player is currently being trained
randomTheta = False #generate random theta values at beginning of training

#Data
gameIterations = 100 #for creating dataset

player1InputDir = "data/player1/input.txt" #Red guy
player1OutputDir = "data/player1/output.txt"
player1EpsilonDir = "data/player1/epsilon.txt"
player1ThetaDir = "data/player1/theta.txt"

player2InputDir = "data/player2/input.txt" #Yellow guy
player2OutputDir = "data/player2/output.txt"
player2EpsilonDir = "data/player2/epsilon.txt"
player2ThetaDir = "data/player2/theta.txt"
