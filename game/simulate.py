from random import randrange
import Config
import time

end = False
def endStatus():
    return end
def setEndStatus(newStatus):
    global end
    end = newStatus

def simulate(rounds, buttons):
    print(buttons)
    time.sleep(3)
    print("beginning simulation")
    iterations = 0
    while iterations < rounds:
        print("round: {}".format(iterations))

        while not endStatus():
            buttons[randrange(7)].invoke()
            time.sleep(.2)
        print("finished round {}".format(iterations))
        iterations += 1
        setEndStatus(False)
