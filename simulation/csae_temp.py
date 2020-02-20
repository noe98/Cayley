"""
@author: Justin Pusztay
In this file we define a class that represents the nearest
neighbor transition rate.
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['CSAE_TEMP']

from Cayley.classes.spinsimulation import *
import random
import numpy as np

class CSAE_TEMP(SpinSimulation):

    def __init__(self,network,trials,timesteps):
        SpinSimulation.__init__(self,network,trials,timesteps)

    def simulate(self,j,k,temperatures):
        for trial in range(self.trials):
            for timestep in range(1,self.timesteps):
                for node in self.network:
                    state = self.data[trial,timestep-1,node]
                    beta = (1/temperatures[node])
                    neighbor_sum = self.sumOfNeighbors(node,timestep-1,trial)
                    probability = 0.5*(1-state*np.tanh(beta*J*neighbor_sum))
                    random_num = random.uniform(0,1)
                    if state == 1 and random_num <= probability:
                        self.data[trial,timestep,node] = -1
                    elif state == -1 and random_num <= probability:
                        self.data[trial,timestep,node] = 1
                    else:
                        self.data[trial,timestep,node] = state
