import numpy as np
import Config

from network.functions import cost
from network.functions import hypothesis
from network.functions import computeGradient

np.set_printoptions(edgeitems=30, linewidth=100000)

x = np.array(([0,0],
             [0,1],
             [1,0],
             [1,1])) #0,1,1,0

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
y = np.array(([1,0],
              [0,1],
              [0,1],
              [1,0])) #[False,True]

h0 = np.array((0.999,0.001,0.001,0.999))
h1 = np.array((0.001,0.999,0.999,0.001))

hypothesis0 = hypothesis.hypothesis(x[0], t)
gradient = computeGradient.computeGradient(x[0], t, y[0])
#
# cost0 = cost.cost(h0,y)
# cost1 = cost.cost(h1,y)
