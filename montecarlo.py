"""
Authors: Justin Pusztay, Matt Lubas, and Griffin Noe
Filename: montecarlo.py
Project: Research for Irina Mazilu, Ph.D.

This file contains the MonteCarlo class. It creates a Cayley Tree and performs
a MonteCarlo simullation on it. Also there exists methods that allow data
to be analyzed and exported.
"""

import random
import xlsxwriter #http://xlsxwriter.readthedocs.io/tutorial01.html 
from cayleytree import CayleyTree

class MonteCarlo(object):
    
    def __init__(self, generations, links,
                 alpha = .5, beta = .8, gamma = .2):
        """Runs the Monte Carlo simulation the desired number of times."""
        self.tree = CayleyTree(generations, links)
        self.generations = generations
        self.links = links
        self.state_d = dict()
        self.list_cache = None
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def getAlpha(self):
        """Returns alpha value."""
        return self.alpha

    def getBeta(self):
        """Returns beta value."""
        return self.beta
    
    def getGamma(self):
        """Returns gamma value."""
        return self.gamma

    def getListCache(self):
        """Returns the list cache."""
        return self.list_cache

    def getStates(self):
        """Returns the state_d dictionary."""
        return self.state_d

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
        sumOfStates = 0
        for x in self.tree.fastLinkCreator()[node]:
            sumOfStates += state_d.get(x)
        return sumOfStates

    def densityCalculator(self,gen,state_d):
        """Takes a generation and a state dictionary and returns the density
           of the generation."""
        nodes = self.tree.nodeFinder(gen)
        density = 0
        for node in nodes:
            density += state_d.get(node)
        return density 
            
    def simulate(self):
        """Simulates the Monte Carlo simulation on the Cayley Tree for one
           time step and stores that data."""
        time_steps = range(len(self.state_d)) 
        if self.list_cache == None:
            list_cache = list()
            list_cache.append(self.state_d)
        else:
            list_cache = self.list_cache
        cache = dict()
        for x in range(len(self.getStates())):
            summ = self.nearestNeighborCalculator(x,list_cache[-1])
            print("summ: ", summ)
            probability = self.gamma*list_cache[-1][x] + \
                                    (1 - list_cache[-1][x])*\
                                    self.alpha*(self.beta**(summ))
            if random.uniform(0, 1) <= probability and list_cache[-1][x] == 0:
                cache[x] = 1
            elif random.uniform(0, 1) <= probability and \
                 list_cache[-1][x] == 1:
                cache[x] = 0 
            else:
                cache[x] = list_cache[-1][x]
               

        print("cache: ",cache)
        list_cache.append(cache)
        self.list_cache = list_cache
        return self.list_cache

    def sendExcel(self):
        """A file that sends the data ran from the most recent
           MonteCarlo().simulate to an excel sheet. Must run the simulate
           method in order to have this method work."""

        #If File exists, load file. If sheet 1 is occupied, create a second
        #sheet. Rename / use input for naming sheet.
        
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

        
