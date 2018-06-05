"""
Filename: montecarlo.py
Project: Research for Irina Mazilu, Ph.D.
This file contains the MonteCarlo class. It creates a Cayley Tree and performs
a MonteCarlo simullation on it. Also there exists methods that allow data
to be analyzed and exported.
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)',
                        'Matt Lubas (lubasm18@mail.wlu.edu)',
                        'Griffin Noe (noeg21@mail.wlu.edu)'])

__all__ = ['MonteCarlo']

import random
import xlsxwriter #http://xlsxwriter.readthedocs.io/tutorial01.html 
from Cayley.cayleytree import *
from Cayley.lattice import *

class MonteCarlo(object):
    
    def __init__(self, network,
                 alpha = .5, beta = .8, gamma = 0.0, mu = 0.3,
                 r1 = 0.3, r2 = 0.5):
        """Runs the Monte Carlo simulation the desired number of times."""
        self.network = network
        self.state_d = dict() ## Is dict. w/ node# key
        self.list_cache = None ## Is array w/ timestep first index, node# second
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.mu = mu
        self.r1 = r1
        self.r2 = r2
        self.user_input = None
        
    def getAlpha(self):
        """Returns alpha value."""
        return self.alpha

    def getBeta(self):
        """Returns beta value."""
        return self.beta
    
    def getGamma(self):
        """Returns gamma value."""
        return self.gamma

    def getMu(self):
        """Returns mu value"""
        return self.mu
        
    def getR1(self):
        """Returns r1 value"""
        return self.r1

    def getR2(self):
        """Returns r2 value"""
        return self.r2
    
    def getListCache(self):
        """Returns the list cache."""
        return self.list_cache

    def getStates(self):
        """Returns the state_d dictionary."""
        return self.state_d

    #Initial State Methods
    def emptyDictionary(self):
        """Sets the initial state of the nodes to empty, a value of 0, in the
           state dictionary."""
        for x in self.network:
            self.state_d[x] = 0
        return self.state_d

    def randomDictionary(self):
        """Assigns a filled state, a value of 1, to a random number of nodes in the
           state dictionary."""
        random_num = random.randint(0,self.network.nodeNumber())
        for x in self.network:
            if random.randint(0,self.network.nodeNumber()) <= random_num:
                self.state_d[x] = 0
            else:
                self.state_d[x] = 1
        return self.state_d

    def zeroDictionary(self):
        """Assigns a filled state to the central node, and a zero elsewhere."""
        self.state_d[0] = 1
        for x in self.network:
            self.state_d[x] = 0
        return self.state_d

    #Analysis Methods
    def getZeros(self):
        """Calculates the number of nodes in the empty state- a value of 0."""
        return len(self.state_d) - sum(self.state_d.values())

    def getOnes(self,timestep):
        """Calculates the number of nodes in the filled state- a value of 1."""
        return sum(self.list_cache[timestep].values())

    def neighborSum(self,node,state_d):
        """Takes the node number and caculates the sum of the nearest nieghbors.
           This method returns the sum of the states of the nearest neigbhors.
           This algorithm has a running time of $O(n)$ for $n$ nearest neigbhors
           for a given node.
           Parameters
           ----------
           node: node
                 A node's name can be any hashable object, like an int, float,
                 or str.
           state_d: dictionary
                    A dictionary that contains each node as a key and the state
                    as a value.
           Returns
           -------
           The sum of the stetes of the nearest neighbor of a node.
           Examples
           --------
           >>> import Cayley as cy
           >>> g = cy.Graph()
           >>> g.add('a')
           >>> g.add('b')
           >>> g.add('c')
           >>> g.add('d')
           >>> g.linkCreator('a','b')
           >>> g.linkCreator('a','c')
           >>> g.linkCreator('b','d')
           >>> g.linkCreator('c','d')
           >>> mc = cy.MonteCarlo(g)
           >>> mc.randomDictionary()
           {'a': 1, 'b': 0, 'c': 1, 'd': 1}
           >>> mc.neighborSum('b')
           2
        """
        return sum([state_d.get(x)
                    for x in self.network.nearestNeighborFinder(node)])
    
    def edgeSum(self,neighbor,timestep):
        """Gets the state of a node on an edge."""
        return timestep.get(neighbor)

    def density(self,gen,state_d):
        """Takes a generation and a state dictionary and returns the density
           of the generation."""
        if self.network.getType() == "CayleyTree":
            nodes = self.network.nodeFinder(gen)
            density = 0
            for node in nodes:
                density += state_d.get(node)
            return density
        else:
            return TypeError("Inappropriate Arguement Type.")

    #Monte Carlo Algorithm methods 
    def simulateNN(self):
        """A monte carlo method that runs a timestep of a simulation
        by visiting each node.
        This method returns a dictionary of all the nodes and the state that
        each node has. It iterates through the network and applies a probability
        function to each node and generates a random number to try to satisfy
        probability. If satisfied, the state of the node is changed and recorded
        in the dictionary.
        This algorithm has a running time of $O(n)$ for $n$ nodes in a network.
        Returns
        -------
        self.list_cache: a list containing the dictionaries of all the data
                         for each node generated by previous timesteps.
        Notes
        -----
        -> This method only runs a single timestep.
        -> The only states a node can have is 0 (representing full) and 1
           (reprsenting empty)
        -> The process of running a monte carlo iterating through each node
           is that the probability of a node changing state is dependent on
           its nearest neighbors.
        Examples
        --------
        >>> import Cayley as cy
        >>> mc = cy.MonteCarlo(cy.CayleyTree(3,3))
        >>> mc.emptyDictionary()
        >>> mc.simulateNN() #runs one timestep
        To run multiple timesteps:
        >>> import Cayley as cy
        >>> mc = cy.MonteCarlo(cy.CayleyTree(3,3))
        >>> mc.emptyDictionary()
        >>> for count in range(10): #runs 10 timesteps
                 mc.simulateNN()
        """
        if self.list_cache == None:
            list_cache = list()
            list_cache.append(self.state_d)
        else:
            list_cache = self.list_cache
        cache = dict()
        for x in self.network:
            summ = self.neighborSum(x,list_cache[-1])
            #print("summ: ", summ)
            probability = self.gamma*list_cache[-1][x] + \
                                    (1 - list_cache[-1][x])*\
                                    self.alpha*(self.beta**(summ))
            if list_cache[-1][x] == 0 and \
               random.uniform(0, 1) <= probability:
                cache[x] = 1
            elif list_cache[-1][x] == 1 and \
                 random.uniform(0, 1) <= probability:
                cache[x] = 0 
            else:
                cache[x] = list_cache[-1][x]
        #print("cache: ",cache)
        list_cache.append(cache)
        self.list_cache = list_cache
        #return self.list_cache

    def simulateEI(self):
        """Runs a timestep of a MonteCarlo by picking the edge and then a random
        node on the edge in order to use a probability function in oder to see a
        change of state."""
        if self.list_cache == None:
            list_cache = list()
            list_cache.append(self.state_d)
        else:
            list_cache = self.list_cache
        cache = dict()
        for x in self.network.linksAsTuples():
            node_picked = random.randint(0,1)
            summ = self.edgeSum(x[1-node_picked],list_cache[-1])
            #print("summ: ", summ)
            probability = self.gamma*list_cache[-1][x[node_picked]] + \
                                (1 - list_cache[-1][x[node_picked]])*\
                                (self.r1*summ + self.r2*(1 - summ))
            if random.uniform(0, 1) <= probability and \
               list_cache[-1][x[node_picked]] == 0:
                cache[x[node_picked]] = 1
                if x[1-node_picked] not in cache:
                    cache[x[1-node_picked]] = list_cache[-1][x[1-node_picked]]
            elif random.uniform(0, 1) <= probability and \
                 list_cache[-1][x[node_picked]] == 1:
                cache[x[node_picked]] = 0
                if x[1-node_picked] not in cache:
                    cache[x[1-node_picked]] = list_cache[-1][x[1-node_picked]]
            else:
                cache[x[node_picked]] = list_cache[-1][x[node_picked]]
                if x[1-node_picked] not in cache:
                    cache[x[1-node_picked]] = list_cache[-1][x[1-node_picked]]
        #print("cache: ",cache)
        list_cache.append(cache)
        self.list_cache = list_cache
        return self.list_cache

    def simulateTL(self,timestep): #Only works for first timestep
        """Simulates the Monte Carlo simulation on the Cayley Tree for one
           time step and stores that data."""
        #print("Timestep: " + str(timestep))
        time_steps = range(len(self.state_d))
##        f=1#sho
##        for x in range(1,self.network.generations+1):#sho
##            f= f+ self.network.links*(self.network.links-1)**(x-1)#sho
##        #print("f: " +str(f))
        if self.list_cache == None:
            list_cache = list()
            list_cache.append(self.state_d)
        else:
            list_cache = self.list_cache
        cache = dict()
        #no_nodes = (self.network.links*(self.network.links-1)**(self.network.generations-1))
        nodes = len(self.network)
        if timestep == 0:
            dens = 0 #density function
        else:
            dens = self.getOnes(timestep)/nodes ### make sure this calls correct timestep
        #print("dens: " +str(dens))
        for x in self.network:
            probability = self.gamma*list_cache[-1][x] + \
                                    (1 - list_cache[-1][x])*(1-dens)*self.mu
            #print("probability: " +str(probability))
            if random.uniform(0, 1) <= probability and list_cache[-1][x] == 0:
                cache[x] = 1
            elif random.uniform(0, 1) <= probability and \
                 list_cache[-1][x] == 1:
                cache[x] = 0 
            else:
                cache[x] = list_cache[-1][x]
        #print("cache: ",cache)
        list_cache.append(cache)
        self.list_cache = list_cache
        return self.list_cache

    def clear(self):
        """Clears the data from the tree."""
        self.state_d = dict()
        self.list_cache = None

    #Data Export Methods
    def sendExcel(self,filename = "monteCarloData.xlsx"):
        """A file that sends the data ran from the most recent
           MonteCarlo().simulate to an excel sheet. Must run the simulate
           method in order to have this method work."""

        #If File exists, load file. If sheet 1 is occupied, create a second
        #sheet. Rename / use input for naming sheet.
        
        if self.list_cache == None:
            raise ValueError("No data to send to excel. Must run simulation")
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet("Monte Carlo Data")
        worksheet.write(0,0,"Timestep")
        for x in range(len(self.state_d)):
            worksheet.write(x+1,0,"Node "+ str(self.network.keys[x]))
        for y in range(len(self.state_d)):
            worksheet.write(0,y+1,str(y))
        for y in range(len(self.list_cache)):
            for x in range(self.network.nodeNumber()):
                worksheet.write(x+1,y+1,self.list_cache[y][self.network.keys[x]])
        if self.network.getType() == "CayleyTree":
            worksheet2 = workbook.add_worksheet("Density")
            worksheet2.write(0,0,"Timestep")
            for x in range(self.network.generations+1):
                worksheet2.write(x+1,0,"Gen. "+str(x))
            for y in range(len(self.state_d)):
                worksheet2.write(0,y+1,str(y))
            for y in range(len(self.list_cache)):
                for x in range(self.network.generations+1):
                    worksheet2.write(x+1,y+1,self.density(x,self.list_cache[y]))
            workbook.close()
        else:
            workbook.close()
