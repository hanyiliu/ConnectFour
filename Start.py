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

a = 0.001 #alpha value

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

c = 0
for j in range(0,1000):
    for i in range(0, np.shape(x)[0]):
        hypothesis0 = hypothesis.hypothesis(x[i], t)
        gradient = computeGradient.computeGradient(x[i], t, y[i])

        cost0 = cost.cost(hypothesis0,y[i])

        #
        # print("input: {}".format(x[i]))
        # print("hypothesis: {}".format(hypothesis0))
        # print("actual: {}".format(y[i]))
        # print("cost: {}".format(cost0))

        thetaList[0] = thetaList[0] - a*gradient[0]
        thetaList[1] = thetaList[1] - a*gradient[1]
        thetaList[2] = thetaList[2] - a*gradient[2]
        t = thetaList

        c = cost0

    print(c)

print("finished, final results:")
print(hypothesis.hypothesis(x[0],t))
print(hypothesis.hypothesis(x[1],t))
print(hypothesis.hypothesis(x[2],t))
print(hypothesis.hypothesis(x[3],t))




# hypothesis0 = hypothesis.hypothesis(x[i], t)
# gradient = computeGradient.computeGradient(x[0], t, y[i])
#
# cost0 = cost.cost(hypothesis0,y[i])
#
#
# print("input: {}".format(x[i]))
# print("hypothesis: {}".format(hypothesis0))
# print("actual: {}".format(y[i]))
# print("cost: {}".format(cost0))
#
#
#
# hypothesis1 = hypothesis.hypothesis(x[i], t)
# cost1 = cost.cost(hypothesis1, y[i])
#
# print("hypothesis: {}".format(hypothesis1))
# print("actual: {}".format(y[i]))
# print("cost: {}".format(cost1))
#
# print("theta shape: {}, {}, {}".format(np.shape(thetaList[0]), np.shape(thetaList[1]), np.shape(thetaList[2])))
# print("gradient shape: {}, {}, {}".format(np.shape(gradient[0]), np.shape(gradient[1]), np.shape(gradient[2])))
