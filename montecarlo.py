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
import numpy as np

class MonteCarlo(object):
    
    def __init__(self, network,
                 alpha = .5, beta = .8, gamma = 0.0, mu = 0.3,
                 r1 = 0.3, r2 = 0.5):
        """Runs the Monte Carlo simulation the desired number of times."""
        self.__network = network
        self.__sim_data = list()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.mu = mu
        self.r1 = r1
        self.r2 = r2
        
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

    def getTimesteps(self): #needs to be looked at in 0 case
        """Returns the number of timesteps."""
        return len(self.__sim_data)

    #Initial State Methods
    def emptyDictionary(self): #startEmpty
        """Creates a dictionary where all nodes have an initial state of zero.
        This will append a dictionary to the sim_data instance variable.

        Returns
        -------
        self.__sim_data with a new dictionary with all the nodes with an initial
        empty state.

        Raises
        ------
        ValueError: If size of self.__sim_data is not 0

        Notes
        -----
        -> This is an intial state method, meaning that it can only be used
           when there is no data in sim_data, meaning the list has a lenght
           of zero. 

        Examples
        --------
        >>> import Cayley as cy
        >>> mc = cy.MonteCarlo(Lattice(2,2))
        >>> mc.emptyDictionary()
        {0:0,1:0,2:0,3:0}
        """
        if len(self.__sim_data) == 0:
            self.__network.addMultipleNodes(self.__network,state=0)
            self.__sim_data.append(self.__network.getNodeFeature('state'))
        else:
            raise ValueError("Must clear data before setting initial state.")

    def randomDictionary(self): #startRandom
        """Assigns an initial filled state, a value of 1, to a
        random number of nodes in the network.

        Returns
        -------
        self.__sim_data with a new dictionary with all the nodes with an initial
        random state.

        Raises
        ------
        ValueError: If size of self.__sim_data is not 0

        Notes
        -----
        -> This is an intial state method, meaning that it can only be used
           when there is no data in sim_data, meaning the list has a lenght
           of zero. 

        Examples
        --------
        >>> import Cayley as cy
        >>> mc = cy.MonteCarlo(Lattice(2,2))
        >>> mc.randomDictionary()
        {0:1,1:0,2:1,3:0}
        """
        if len(self.__sim_data) == 0:
            for node in self.__network:
                self.__network.add(node,state = random.randint(0,1))
            self.__sim_data.append(self.__network.getNodeFeature('state'))
            return  self.__sim_data
        else:
            raise ValueError("Must clear data before setting initial state.")

    def zeroDictionary(self):
        """Assigns an initial filled state, a value of 1, to a
         central node.

        Returns
        -------
        self.__sim_data with a new dictionary with thee central node with
        an initial filled state and all other nodes with an empty state.

        Raises
        ------
        ValueError: If size of self.__sim_data is not 0.
        AttributeError: If network is not a Cayley Tree.

        Notes
        -----
        -> This is an intial state method, meaning that it can only be used
           when there is no data in sim_data, meaning the list has a lenght
           of zero.
        -> This only applies to Cayley Tree networks.

        Examples
        --------
        >>> import Cayley as cy
        >>> mc = cy.MonteCarlo(CayleyTree(2,2))
        >>> mc.emptyDictionary()
        {0:1,1:0,2:0,3:0,4:0}
        """
        if len(self.__sim_data) == 0:
            self.__network.addMultipleNodes(self.__network,state=0)
            self.__network.add(0,state = 1)
            self.__sim_data.append(self.__network.getNodeFeature('state'))
        else:
            raise ValueError("Must clear data before setting initial state.")

    def startFull(self):
        """Sets the inital state of all nodes to full."""
        if len(self.__sim_data) == 0:
            self.__network.addMultipleNodes(self.__network,state=1)
            self.__sim_data.append(self.__network.getNodeFeature('state'))
        else:
            raise ValueError("Must clear data before setting initial state."

    def magnetization(self,nodes):
        """Adds magnetization to a certain group of nodes."""
        if len(self.__sim_data) == 0:
            self.__network.addMultipleNodes(nodes,magnetization=0)
        else:
            raise ValueError("Must clear data before setting initial state.")

    def temperature(self,nodes,temp):
        """Adds a temperature to a group of nodes."""
        self.__network.addMultipleNodes(nodes,temperature=temp)
                
    #Analysis Methods
    def getZeros(self,timestep):
        """Finds the number of nodes with in the empty state at any given
        timestep.

        This algorithm has a running time of $O(1)$.

        Parameters
        ----------
        timestep: integer
            An integer that represents the timestep to calculate the number
            of nodes in the empty state.

        Returns
        -------
        The number of nodes in empty state.

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
        >>> mc.getZeros(0)
        1
        """
        return len(self.__sim_data[timestep]) - self.getOnes(timestep)

    def getOnes(self,timestep):
        """Finds the number of nodes with in the filled state at any given
        timestep.

        This algorithm has a running time of $O(1)$.

        Parameters
        ----------
        timestep: integer
            An integer that represents the timestep to calculate the number
            of nodes in the filled state.

        Returns
        -------
        The number of nodes in filled state.

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
        >>> mc.getOnes(0)
        3
        """
        return sum(self.__sim_data[timestep].values())

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
                    for x in self.__network.neighborFinder(node)])
    
    def edgeSum(self,neighbor,timestep):
        """Gets the state of a node on an edge."""
        return timestep.get(neighbor)

    def density(self,gen,state_d):
        """Takes a generation and a state dictionary and returns the density
           of the generation."""
        try:
            nodes = self.__network.nodesPerGen(gen)
            density = 0
            for node in nodes:
                density += state_d.get(node)
            return density
        except AttributeError:
            return "Inappropriate network type"

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
        self.__sim_data: a list containing the dictionaries of all the data
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

        if len(self.__sim_data) == 0:
            raise ValueError("Must set up initial state of simulation")
        list_cache = self.__sim_data
        cache = dict()
        for x in self.__network:
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
        self.__sim_data = list_cache
        return self.__sim_data

    def simulateEI(self):
        """Runs a timestep of a MonteCarlo by picking the edge and then a random
        node on the edge in order to use a probability function in oder to see a
        change of state."""
        if len(self.__sim_data) == 0:
            raise ValueError("Must set up initial state of simulation")
        list_cache = self.__sim_data
        cache = dict()
        for x in self.__network.linksAsTuples():
            node_picked = random.randint(0,1)
            summ = self.edgeSum(x[1-node_picked],list_cache[-1])
            #print("summ: ", summ)
            probability = self.gamma*list_cache[-1][x[node_picked]] + \
                                (1 - list_cache[-1][x[node_picked]])*\
                                (self.r1*summ + self.r2*(1 - summ))
            if list_cache[-1][x[node_picked]] == 0 and \
               random.uniform(0, 1) <= probability: 
                cache[x[node_picked]] = 1
                #check to see if state of neighbor has changed before setting
                #to original
                if x[1-node_picked] not in cache:
                    cache[x[1-node_picked]] = list_cache[-1][x[1-node_picked]]
            elif list_cache[-1][x[node_picked]] == 1 and \
                 random.uniform(0, 1) <= probability:                  
                cache[x[node_picked]] = 0
                if x[1-node_picked] not in cache:
                    cache[x[1-node_picked]] = list_cache[-1][x[1-node_picked]]
            else:
                cache[x[node_picked]] = list_cache[-1][x[node_picked]]
                if x[1-node_picked] not in cache:
                    cache[x[1-node_picked]] = list_cache[-1][x[1-node_picked]]
        #print("cache: ",cache)
        list_cache.append(cache)
        self.__sim_data = list_cache
        return self.__sim_data
    
    def simulateTL(self,timestep): #Only works for first timestep
        """Simulates the Monte Carlo simulation on the Cayley Tree for one
           time step and stores that data."""
        #print("Timestep: " + str(timestep))
        #no_nodes = (self.__network.links*(self.__network.links-1)**(self.__network.generations-1))
        if len(self.__sim_data) == 0:
            raise ValueError("Must set up initial state of simulation")
        list_cache = self.__sim_data
        cache = {}
        nodes = len(self.__network)
        if timestep == 0:
            dens = 0 #density function
        else:
            dens = self.getOnes(timestep)/nodes ### make sure this calls correct timestep
        #print("dens: " +str(dens))
        for x in self.__network:
            probability = self.gamma*list_cache[-1][x] + \
                                    (1 - list_cache[-1][x])*(1-dens)*self.mu
            #print("probability: " +str(probability))
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
        self.__sim_data = list_cache
        return self.__sim_data

    def simulateTemp(self, k = 1, J = 1):
        """Simulates the Monte Carlo simulation on the Cayley Tree for one
           time step and stores that data. Uses temperature of nodes in
           calculation of probabilty."""
        if len(self.__sim_data) == 0:
            raise ValueError("Must set up initial state of simulation")
        list_cache = self.__sim_data
        cache = dict()
        temps = self.__network.getNodeFeature('temperature')
        for x in self.__network:
            beta = (1/k)*temps[x]
            summ = self.neighborSum(x,list_cache[-1])
            #print("summ: ", summ)
            probability = 0.5*(1-list_cache[-1][x]*np.tanh(beta*J*summ))
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
        self.__sim_data = list_cache
        return self.__sim_data

    def clear(self):
        """Clears the data from the tree."""
        self.__sim_data = list()

    #Data Export Methods
    def simData(self,timestep):
        """Returns the sim data at a certain timestep."""
        return self.__sim_data[timestep]
    
    def sendExcel(self,filename = "monteCarloData.xlsx"):
        """A file that sends the data ran from the most recent
           MonteCarlo().simulate to an excel sheet. Must run the simulate
           method in order to have this method work."""

        #If File exists, load file. If sheet 1 is occupied, create a second
        #sheet. Rename / use input for naming sheet.
        
        if self.__sim_data == list():
            raise ValueError("No data to send to excel. Must run simulation")
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet("Monte Carlo Data")
        worksheet.write(0,0,"Timestep")
        for x in range(len(self.__sim_data[0])):
            worksheet.write(x+1,0,"Node "+ str(self.__network.keys[x]))
        for y in range(len(self.__sim_data[0])):
            worksheet.write(0,y+1,str(y))
        for y in range(len(self.__sim_data)):
            for x in range(self.__network.nodeNumber()):
                worksheet.write(x+1,y+1,self.__sim_data[y][self.__network.keys[x]])
        if self.__network.getType() == "CayleyTree":
            worksheet2 = workbook.add_worksheet("Density")
            worksheet2.write(0,0,"Timestep")
            for x in range(self.__network.generations+1):
                worksheet2.write(x+1,0,"Gen. "+str(x))
            for y in range(len(self.__sim_data[0])):
                worksheet2.write(0,y+1,str(y))
            for y in range(len(self.__sim_data)):
                for x in range(self.__network.generations+1):
                    worksheet2.write(x+1,y+1,self.density(x,self.__sim_data[y]))
            workbook.close()
        else:
            workbook.close()
