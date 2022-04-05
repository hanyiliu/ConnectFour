import numpy as np
import Config

t = np.random.uniform(-1, 1, (Config.networksize[1]+1,Config.networksize[0],Config.networksize[0]+1)) #[# of layers, # of neurons, # of neurons + 1 to account for bias unit]

print(np.shape(t))
thetaList = []
for i in range(0, np.shape(t)[0]):
    if i == 0: #Fix first layer to account for input units
        thetaList.append(t[0,:,0:Config.input+1])
    elif i == np.shape(t)[0]-1: #Fix last layer to account for output units
        thetaList.append(t[-1,0:Config.output])
    else:
        thetaList.append(t[i])

t = thetaList

flatThetas = np.concatenate([t[0].flatten(),t[1].flatten(),t[2].flatten()])


np.savetxt(Config.player2ThetaDir, flatThetas) #Overwrites current theta values. TODO: fix numpy conversion
