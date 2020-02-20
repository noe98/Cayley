"""
@author: Justin Pusztay
In this class we define a class that reprsents all of the pariticle
simulations.
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['ParticleSimulation']

import numpy as np
import random
from Cayley.classes.abstractsimulation import *

class ParticleSimulation(AbstractSimulation):

    def __init__(self,network,trials,timesteps):
        AbstractSimulation.__init__(self,network,trials,timesteps)

    def startEmpty(self):
        """
        Sets the initial states of the particles to 0, meaning empty.
        """
        self.data[0:self.trials,0] = np.zeros(len(self.network))

    def startRandom(self):
        """
        Sets the initial states of the particles to 0 or 1.
        """
        self.data[0:self.trials,0] = np.random.randint(2, size = len(self.network))

    def startCentralFull(self):
        """
        Assigns an initial filled state, a value of 1, to a
        central node and 0 elsewhere.
        """
        self.data[0:self.trials,0,0] = 1

    def startFull(self):
        """Starts the state of all the vertices as full, meaning 1."""
        self.data[0:self.trials,0] = np.ones(len(self.network))

    def countFull(self,trial,timestep):
        """
        Using the default trial at 0, it counts the number of non zero elements
        in the vector representing the timestep.
        """
        return np.count_nonzero(self.data[trial,timestep])

    def countEmpty(self,timestep,trial = 0):
        """
        Using the default trial at 0, it counts the number of zero elements
        in the vector representing the timestep.
        """
        return self.data[timestep,trial].size - self.count_full(timestep,trial)

    def sumOfEmptyNeighbors(self,trial,timestep,node):
        """
        Returns the number of neighbors to a node that have state 0.
        """
        zero_sum = 0
        for item in self.network.getNeighbor(node):
            zero_sum += (1 - self.data[trial,timestep,item])
        return zero_sum

    def checkProbability(self,trial,timestep,node,probability,state):
        random_num = random.uniform(0,1)
        if state == 0 and random_num <= probability:
            self.data[trial,timestep,node] = 1
        elif state == 1 and random_num <= probability:
            self.data[trial,timestep,node] = 0
        else:
            self.data[trial,timestep,node] = state
