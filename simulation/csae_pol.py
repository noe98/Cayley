"""
@author: Justin Pusztay
In this file we define a class that represents the transition rate that
is used for simulating political systems.
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['CSAE_POL']

from Cayley.classes.particlesimulation import *
import random
import numpy as np

class CSAE_POL(ParticleSimulation):

    def __init__(self,network,trials,timesteps):
        ParticleSimulation.__init__(self,network,trials,timesteps)

    def simulate(self, alpha,beta,gamma,beta_senator, phi_senator):
        for trial in range(self.trials):
            for timestep in range(1,self.timesteps):
                for node in self.network:
                    state = self.data[trial,timestep-1,node]
                    opposite_state = self.sumOfEmptyNeighbors(node,timestep-1,trial)
                    neighbor_sum = self.sumOfNeighbors(node,timestep-1,trial)
                    phi = phi_senator[node]
                    beta = beta_senator[node]
                    probability = gamma*state*(phi**(opposite_state/ \
                                  self.network.degree(node))) + (1-state)*\
                                  alpha*(beta**neighbor_sum/self.network.degree(node)) 
                    self.checkProbability(trial,timestep,node,probability,state)    
