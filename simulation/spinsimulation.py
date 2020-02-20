"""
@author: Justin Pusztay
In this class we define a class that reprsents all of the spin
simulations.
"""

import numpy as np
from Cayley.classes.abstractsimulation import *

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['SpinSimulation']



class SpinSimulation(AbstractSimulation):

    def __init__(self, network,trials,timesteps):
        AbstractSimulation.__init__(self,network)
        
    def startUp(self):
        """Sets the inital state of all nodes to 1 or spin up."""
        self.data[0:self.trials,0] = np.ones(len(self.network))

    def startDown(self):
        """Sets the inital state of all nodes to -1 or spin down."""
        self.data[0:self.trials,0] = np.full(len(self.network),-1)

    def startRandom(self):
        """
        Sets the initial states of the particles to -1 or 1.
        """
        self.data[0:self.trials,0] = np.random.choice([-1,1], size = len(self.network))

    def countUp(self,timestep,trial):
        return np.count_nonzero(self.data[trial,timestep] == 1)

    def countDown(self,timestep,trial):
        return np.count_nonzero(self.data[trial,timestep] == -1)
