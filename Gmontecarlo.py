"""
Authors: Justin Pusztay, Matt Lubas, and Griffin Noe
Filename: montecarlo.py

This file contains the MonteCarlo class. It creates a Cayley Tree and performs
a MonteCarlo simullation on it. Also there exists methods that allow data
to be analyzed and exported.
"""

import random
import xlsxwriter #http://xlsxwriter.readthedocs.io/tutorial01.html 
from cayleytree import CayleyTree

class MonteCarlo(object):

    #Note to Matt and Griffin:
    #state_d will be the new initial dictionary with the three possibilites:
    #all from empty, random % filled, and the 0 node is filled
    #graph will now be self.tree.linkCreator()
    
    def __init__(self, generations, links,
                 alpha = .6, beta = .4, gamma = .8):
        """Runs the Monte Carlo simulation the desired number of times."""
        self.tree = CayleyTree(generations, links)
        self.generations = generations
        self.links = links
        self.state_d = dict()
        self.list_cache = None
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
##    def setGamma(self,gamma):
##        """Sets the desired gamma value for the monte carlo simulation"""
##        self.gamma = gamma
##        return self.gamma
##
##    def setAlpha(self,alpha):
##        """Sets the desired alpha value for the monte carlo simulation."""
##        self.alpha = alpha
##        return self.alpha
##
##    def setBeta(self,beta):
##        """Sets the desired beta value for the monte carlo simulation."""
##        self.beta = beta
##        return self.beta

    def emptyDictionary(self):
        """Sets the initial state of the nodes to empty, a value of 0, in the
           state dictionary."""
        for x in range(self.tree.nodeNumber()):
            self.state_d[x] = 0
        return self.state_d

    def randomDictionary(self):
        """Assigns a filled state, a value of 1, to a random number of nodes in the
           state dictionary."""
        random_num = random.randint(0,self.tree.nodeNumber())
        for x in range(self.tree.nodeNumber()):
            if random.randint(0,self.tree.nodeNumber()) <= random_num:
                self.state_d[x] = 0
            else:
                self.state_d[x] = 1
        return self.state_d

    def zeroDictionary(self):
        """Assigns a filled state to the central node, and a zero elsewhere."""
        self.state_d[0] = 1
        for x in range(1,self.tree.nodeNumber()):
            self.state_d[x] = 0
        return self.state_d

    def getZeros(self):
        """Calculates the number of nodes in the empty state- a value of 0."""
        return len(self.state_d) - sum(self.state_d.values())

    def getOnes(self):
        """Calculates the number of nodes in the filled state- a value of 1."""
        return sum(self.state_d.values())

    def nearestNeighborCalculator(self,node,state_d):
        """Takes the node number and caculates the sum of the neartest
           nieghbors."""
        sum_of_neighbors = 0
        for node in self.nearestNeighborFinder(node):
            sum_of_neighbors += state_d[node]
        return sum_of_neighbors

    def nearestNeighborFinder(self,node):
        """Finds the nodes that are neighbors to the node in question."""
        neighbors = list(filter(lambda x: x.count(node) > 0, self.tree.linkCreator()))
        neighbors_list = list()
        for x in neighbors:
            if x[0] != node:
                neighbors_list.append(x[0])
            elif x[1] != node: 
                neighbors_list.append(x[1])
        return neighbors_list

    def simulate(self):
        """Simulates the Monte Carlo simulation on the Cayley Tree. Runs the
           simulation an equal number of times to the number of nodes in the
           tree. Returns a list filled with dictionaries, each containing the state
           of each node after a certain timestep."""
        time_steps = range(len(self.state_d)) #should this be optional variable?
        list_cache = list()
        list_cache.append(self.state_d)
        for n in time_steps:
            cache = dict()
            for x in time_steps:
                summ = self.nearestNeighborCalculator(x,list_cache[n])
                #print("summ: ", summ)
                transition_rate_prob = self.gamma*list_cache[n][x] + \
                                       (1 - list_cache[n][x])*self.alpha*(self.beta\
                                                                          **(summ))
                if random.uniform(0, 1) <= transition_rate_prob and list_cache[n][x] == 0:
                    cache[x] = 1 
                elif random.uniform(0, 1) <= transition_rate_prob and \
                     list_cache[n][x] == 1:
                    cache[x] = 0 
                else:
                    cache[x] = list_cache[n][x]
                
            #print("cache: ",cache)
            list_cache.append(cache)
        self.list_cache = list_cache
        return self.list_cache

    def sendExcel(self):
        """A file that sends the data ran from the most recent
           MonteCarlo().simulate to an excel sheet. Must run the simulate
           method in order to have this method work."""
        if self.list_cache == None:
            raise ValueError("No data to send to excel. Must run simulation")
        workbook = xlsxwriter.Workbook('monteCarloData.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0,"Timestep")
        for x in range(len(self.state_d)):
            worksheet.write(x+1,0,"Node "+str(x))
        for y in range(len(self.state_d)):
            worksheet.write(0,y+1,str(y))
        for y in range(len(self.list_cache)):
            for x in range(self.tree.nodeNumber()):
                worksheet.write(x+1,y+1,self.list_cache[y][x])
##        for x in range(len(self.state_d)):
##            worksheet.write(len(self.state_d)+1,x+1,"=SUM(B1:B4)")
        workbook.close()
