import numpy as np
import Config
from network.functions import hypothesis
from network.functions import reform

def sigmoid(z):
    #print(-z)
    return 1.0 / (1.0 + np.exp(-z.astype(np.longdouble)))
def sigmoidGradient(z):
    return sigmoid(z)*(1-sigmoid(z));

def computeGradient(t, x, y, flattenGradient=False): #For only one input and output right now

    if isinstance(t,np.ndarray) and np.size(np.shape(t)) == 1:
        print("gradient yes")
        t = reform.reformTheta(t) #for bfgs, whose theta input is flattened

    h,a,z = hypothesis.hypothesis(t, x, computingGradient=True) #Step 1

    deltaList = []

    print("gradient shapes:")
    print("x: {}".format(np.shape(x)))
    print("y: {}".format(np.shape(y)))
    print("theta: {}".format(len(t)))

    #This goes backwards (back-propagation)
    delta = a[-1]-y #for output units
    deltaList.insert(0, delta) #delta 4



    z[1] = np.insert(z[1], 0, 1, axis=0) #add 0 to account for bias unit
    delta = np.dot(t[2].T,delta)*sigmoidGradient(z[1])
    delta = np.delete(delta, 0) #remove bias unit's delta
    deltaList.insert(0, delta) #delta 3


    z[0] = np.insert(z[0], 0, 1, axis=0) #add 0 to account for bias unit
    delta = np.dot(t[1].T,delta)*sigmoidGradient(z[0])
    delta = np.delete(delta, 0) #remove bias unit's delta
    deltaList.insert(0, delta) #delta 2 (does not need delta 1)

    gradient0 = np.dot(np.array([deltaList[0]]).T,np.array([a[0]]))
    gradient1 = np.dot(np.array([deltaList[1]]).T,np.array([a[1]]))
    gradient2 = np.dot(np.array([deltaList[2]]).T,np.array([a[2]]))

    gradientList = [gradient0, gradient1, gradient2]

    # if flattenGradient:
    flattenGradient = np.concatenate((gradient0.flatten(),gradient1.flatten(),gradient2.flatten()))
    print("returning shape: {}".format(np.shape(flattenGradient)))
    return flattenGradient
    # else:
    #     return gradientList
