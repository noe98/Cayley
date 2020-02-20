"""
@author: Justin Pusztay
In this file we define a class that represents the total
lattice transition rate.
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['CSAE_TL']

from Cayley.classes.particlesimulation import *
import random
import numpy as np

class CSAE_TL(ParticleSimulation):

    def __init__(self,network,trials,timesteps):
        ParticleSimulation.__init__(self,network,trials,timesteps)

    def simulate(self,gamma,mu):
        for trial in range(self.trials):
            for timestep in range(1,self.timesteps):
                density = self.density(trial,timestep - 1)
                for node in self.network:
                    state = self.data[trial,timestep-1,node]
                    neighbor_sum = self.sumOfNeighbors(node,timestep-1,trial)
                    probability = gamma*state + (1 - state)*(1-density)*mu
                    self.checkProbability(trial,timestep,node,probability,state)


def main():
    import Cayley as cy
    a = cy.CayleyTree(2,2)
    b = CSAE_TL(a,1,10)
    b.startRandom()
    b.simulate(0.2,0.1)
    print(b.data)

if __name__ == "__main__":
    main()
