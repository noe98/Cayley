"""
Authors: Justin Pusztay, Matt Lubas, and Griffin Noe
Filename: montecarlo.py

This file contains the MonteCarlo class. It currently is a subclass of the
CayleyTree class. It takes a Cayley Tree and performs a MonteCarlo simullation
on it. Also there exists methods that allow data to be analyzed and exported.
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import xlwt
import math

from cayleytree import CayleyTree

class MonteCarlo(object):

    #state_d will be the new initial dictionary with the three possibilites
    #graph will be CayleyTree.linkCreator()
    
    def __init__(self, generations, links):
        """Runs the Monte Carlo simulation the desired number of times."""
        self.tree = CayleyTree(generations, links)
        self.generations = generations
        self.links = links
        self.state_d = dict()

    def setGamma(self,gamma):
        """Sets the desired gamma value for the monte carlo simulation"""
        self.gamma = gamma
        return self.gamma

    def setAlpha(self,alpha):
        """Sets the desired alpha value for the monte carlo simulation."""
        self.alpha = alpha
        return self.alpha

    def setBeta(self,beta):
        """Sets the desired beta value for the monte carlo simulation."""
        self.beta = beta
        return self.beta

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

            


##        self.startTest(state_d)
##        if(excel):
##            book,sheet = self.makeExcel(state_d)
##        lyst = self.simulate(state_d,alpha,beta,gamma,graph)
##        if(excel):
##            for n in range(len(lyst)):
##                for x in range(len(lyst[n])):
##                    self.writeExcel(sheet,x,n,lyst[n][x])
##            self.saveExcel(book)
##            self.endTest(state_d,n)

##    def simulate(self, _dict,a,b,g,graph):
##        time_steps = range(len(_dict))
##        list_cache = list()
##        list_cache.append(_dict)
##        for n in time_steps:
##            cache = dict()
##            for x in range(len(_dict)):
##                summ = self.NearestNeighborCalculator(x,list_cache[n],graph)
##                print("summ: ", summ)
##                transition_rate_prob = g*list_cache[n][x] + \
##                                       (1 - list_cache[n][x])*a*(b**(summ))
##                if uniform(0, 1) <= transition_rate_prob and list_cache[n][x] == 0:
##                    cache[x] = 1 #uniform is from random library
##                elif uniform(0, 1) <= transition_rate_prob and \
##                     list_cache[n][x] == 1:
##                    cache[x] = 0 #uniform is from random library
##                else:
##                    cache[x] = list_cache[n][x]
##                
##            print("cache: ",cache)
##            list_cache.append(cache)
##        return list_cache
####            print("Previous cache: ", list_cache[n])
##
####            self.writeExcel(sheet,x,n,state_d[x])
##                            
##    

##
##    def NearestNeighborCalculator(self,node,state_d,graph):
##        """Calculates the sum of the nearest neighbors for a node."""
##        sum_of_neighbors = 0
##        for node in self.NearestNeighborFinder(node,graph):
##            sum_of_neighbors += state_d[node]
##        return sum_of_neighbors
##
##    def NearestNeighborFinder(self,node,graph):
##        """Finds the nodes that are neighbors to the node in question."""
##        neighbors = list(filter(lambda x: x.count(node) > 0, graph))
##        neighbors_list = list()
##        for x in neighbors:
##            if x[0] != node:
##                neighbors_list.append(x[0])
##            elif x[1] != node: 
##                neighbors_list.append(x[1])
##        return neighbors_list
##
##    def makeExcel(self,state_d):
##        book = xlwt.Workbook(encoding="utf-8")
##        sheet1 = book.add_sheet("Sheet 1")
##        rows = list()
##        cols = list()
##        sheet1.write(0,0,"Time Step")
##        
##        for key in state_d:
##            sheet1.write(key+1, 0,"Node " + str(key))
##            sheet1.write(0,key+1, key)
##        return book,sheet1
##
##    def writeExcel(self,sheet,x,n,state):
##        sheet.write(x+1,n+1,state)
##
##    def saveExcel(self,book):
##        book.save("trial.xls")
##
##    def startTest(self,state_d):
##        print("Initial Dictionary")
##        print("--------------------")
##        print(state_d)
##        
##    def endTest(self,state_d,i):
##        print("Dictionary after ", i+1, "runs")
##        print("--------------------------------")
##        print(state_d)
##        print("Number of zeros: ", self.getZeros(state_d))
##        print("Number of ones: ", self.getOnes(state_d))
