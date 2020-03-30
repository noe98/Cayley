#comment
import random

class MonteCarlo(object):

    def __init__(self,network):
        self.network = network
        self.data = list() # list of dictionaries <node, int state> to hold simulation data of each timestep

    def getTimesteps(self):
        """
        Returns the number of timesteps in the current simulation.
        """
        return len(self.data)

    ##### Initial Start States #####

    def startEmpty(self):
        """
        Initializes the network by having the entire network
        with their nodes empty.
        """
        if len(self.data) == 0:
            self.network.setFeature("state",{node:0 for node in self.network})
            self.data.append(self.network.getFeature("state"))
            
    def startFull(self):
        """
        Initializes the network by having the entire network
        with their nodes full.
        """
        if len(self.data) == 0:
            self.network.setFeature("state",{node:1 for node in self.network})
            self.data.append(self.network.getFeature("state"))
                
    def startRandom(self,concentration):
        """
        Initializes the network by having the entire network
        with a certain biased percentage of the network filled
        based the concentration of the nanoparticles initially
        put in.
        """
        if len(self.data) == 0:
            self.network.setFeature("state",{node: 1 if random.uniform(0,1) < concentration else 0 for node in self.network})
            self.data.append(self.network.getFeature("state"))

    #### State Counter Methods ####
                             
    def countEmpty(self,timestep):
        """
        Returns the number of empty nodes in the network.
        """
        return list(self.data[timestep].values()).count(0)

    def countFull(self,timestep):
        """
        Returns the number of full nodes in the network.
        """
        return list(self.data[timestep].values()).count(1)

    def stateDegree(self,node,timestep):
        """
        Returns the state value of the node for its neighbors
        of its degree. 
        """
        return sum([self.data[timestep][node] for node in self.network.getNeighbors(node)])

    #### Density Methods ####

    def density(self,timestep):
        """
        Returns the density of the network at given timestep.
        """
        return self.countFull(timestep) / len(self.network)
