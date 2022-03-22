import numpy as np
import Config
import threading

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
##################################################################

gameThread = threading.Thread(target=simulate.simulate, args=(10, ConnectFour.getButtons()))
gameThread.start()

ConnectFour.main()

np.set_printoptions(edgeitems=30, linewidth=100000)

x = np.array(([0,0],
             [0,1],
             [1,0],
             [1,1])) #0,1,1,0

a = 0.001 #alpha value
m = np.shape(x)[0]

#[5,2]
t = np.random.uniform(-1, 1, (Config.networksize[1]+1,Config.networksize[0],Config.networksize[0]+1)) #[# of layers, # of neurons, # of neurons + 1 to account for bias unit]

thetaList = []
for i in range(0, np.shape(t)[0]):
    if i == 0: #Fix first layer to account for input units
        thetaList.append(t[0,:,0:Config.input+1])
    elif i == np.shape(t)[0]-1: #Fix last layer to account for output units
        thetaList.append(t[-1,0:Config.output])
    else:
        thetaList.append(t[i])

t = thetaList
c = 0 #cost
g = [np.zeros(np.shape(t[0])), np.zeros(np.shape(t[1])), np.zeros(np.shape(t[2]))] #gradient
for j in range(0,1000): #1000 iterations
    for i in range(0, np.shape(x)[0]):
        hypothesis0 = hypothesis.hypothesis(x[i], t)
        gradient = computeGradient.computeGradient(x[i], t, y[i])


        cost0 = cost.cost(hypothesis0,y[i])


        g[0] = g[0] + gradient[0]
        g[1] = g[1] + gradient[1]
        g[2] = g[2] + gradient[2]

        c = cost0
    print(np.shape(t))
    print(np.shape(g))

    t[0] = t[0] - g[0]/m
    t[1] = t[1] - g[1]/m
    t[2] = t[2] - g[2]/m
    g = [np.zeros(np.shape(t[0])), np.zeros(np.shape(t[1])), np.zeros(np.shape(t[2]))]
    print(c)

print("finished, final results:")
print(hypothesis.hypothesis(x[0],t))
print(hypothesis.hypothesis(x[1],t))
print(hypothesis.hypothesis(x[2],t))
print(hypothesis.hypothesis(x[3],t))
