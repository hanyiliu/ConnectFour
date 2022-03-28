from random import randrange
import time

from network.functions import hypothesis
from game import ConnectFour
import Config


end = False
def endStatus():
    return end
def setEndStatus(newStatus):
    global end
    end = newStatus

def reformTheta(t): #takes flattened thetas
    thetaList = []
    print("Reforming theta")
    for i in range(0,Config.networksize[1]+1):


        if i == 0: #input layer
            numberOfThetas = Config.input*(Config.networksize[0]+1)
            theta = np.reshape(t[0:numberOfThetas], (Config.input,Config.networksize[0]+1))
        if i == Config.networksize[1]: #output layer
            numberOfThetas = Config.output*(Config.networksize[0]+1) #should be the same value
            theta = np.reshape(t,(Config.output,Config.networksize[0]+1))
        else: #hidden layers
            numberOfThetas = Config.networksize[0]*(Config.networksize[0]+1)
            theta = np.reshape(t[0:numberOfThetas], (Config.networksize[0],Config.networksize[0]+1))

        print("thetas: {}".format(numberOfThetas))
        t = t[numberOfThetas:]


def simulate(rounds):

    ConnectFour.main()

    time.sleep(3)
    buttons = ConnectFour.getButtons()
    print("beginning simulation")
    iterations = 0

    reformTheta(1)

    while iterations < rounds:
        print("round: {}".format(iterations))

        while not endStatus():
            guess = hypothesis.hypothesis(ConnectFour.getBoard, )
            buttons[randrange(7)].invoke()
            time.sleep(.2)
        print("finished round {}".format(iterations))
        iterations += 1
        setEndStatus(False)
