"""
@author: Justin Pusztay
In this file we define a class that represents the nearest
neighbor transition rate.
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['CSAE_NN']

from Cayley.classes.particlesimulation import *
import random
import numpy as np

class CSAE_NN(ParticleSimulation):

    def __init__(self,network,trials,timesteps):
        ParticleSimulation.__init__(self,network,trials,timesteps)

    def simulate(self, alpha,beta,gamma):
        for trial in range(self.trials):
            for timestep in range(1,self.timesteps):
                for node in self.network:
                    state = self.data[trial,timestep-1,node]
                    neighbor_sum = self.sumOfNeighbors(trial,timestep-1,node)
                    probability = gamma*state + (1-state)*alpha*(beta**neighbor_sum)
                    random_num = random.uniform(0,1)
                    if state == 0 and random_num <= probability:
                        self.data[trial,timestep,node] = 1
                    elif state == 1 and random_num <= probability:
                        self.data[trial,timestep,node] = 0
                    else:
                        self.data[trial,timestep,node] = state
