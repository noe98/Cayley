"""
@author: Justin Pusztay
In this file we create the abstraction of all simulations
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['AbstractSimulation']

import numpy as np

class AbstractSimulation(object):

    def __init__(self,network,trials,timesteps):
        self.data = np.zeros((trials,timesteps,len(network)))
        self.network = network
        self.timesteps = timesteps
        self.trials = trials

    def sumOfNeighbors(self,trial,timestep,node):
        """
        Calculates the sum of the states of the nearest neighbors to the vertex.
        """
        sum_of_states = 0
        for node in self.network.getNeighbors(node):
            sum_of_states += self.data[trial,timestep,node]
        return sum_of_states

    def density(self,trial,timestep):
        """
        Returns the density at a timestep at a particular trial. Meaning the
        number of non-zero elements in the timestep.
        """
        return np.sum(self.data[trial,timestep])/len(self.network)
