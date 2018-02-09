import networkx as nx
import matplotlib.pyplot as plt
from random import *
import xlwt
import math

class MonteCarlo(object):
    
    def __init__(self,state_d,alpha,beta,gamma,excel,graph):
        """Runs the Monte Carlo simulation the desired number of times."""
        #LOOK LATER AT TRANSITION RATE OVERTIME FOR NODE
        #Store previous and new previous in cache for staggered comparison (1)
        print("Initial Dictionary")
        print("--------------------")
        print(state_d)
        time_steps = range(len(state_d))
        if(excel):
            book,sheet = self.makeExcel(state_d)
        #HERE (1)
        for n in time_steps:

            neighbor_state_cache = state_d
            for x in neighbor_state_cache:
                summ = self.NearestNeighborCalculator(x,state_d,graph)
        
                transition_rate_prob = gamma*state_d[x] + \
                                       (1 - state_d[x])*alpha*(beta**(summ))
                #print(transition_rate_prob)
                
                if uniform(0, 1) <= transition_rate_prob and state_d[x] == 0:
                    state_d[x] = 1
                elif uniform(0, 1) <= transition_rate_prob and state_d[x] == 1:
                    state_d[x] = 0
                if(excel):
                    self.writeExcel(sheet,x,n,state_d[x])
            self.endTest(state_d,n)
        if(excel):
            self.saveExcel(book)
            
    def getZeros(self,state_d):
        return len(state_d) - sum(state_d.values())
    
    def getOnes(self,state_d):
        return sum(state_d.values())

    def NearestNeighborCalculator(self,node,state_d,graph):
        """Calculates the sum of the nearest neighbors for a node."""
        sum_of_neighbors = 0
        for node in self.NearestNeighborFinder(node,graph):
            sum_of_neighbors += state_d[node]
        return sum_of_neighbors

    def NearestNeighborFinder(self,node,graph):
        """Finds the nodes that are neighbors to the node in question."""
        neighbors = list(filter(lambda x: x.count(node) > 0, graph))
        neighbors_list = list()
        for x in neighbors:
            if x[0] != node:
                neighbors_list.append(x[0])
            elif x[1] != node: 
                neighbors_list.append(x[1])
        return neighbors_list

    def makeExcel(self,state_d):
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1")
        rows = list()
        cols = list()
        sheet1.write(0,0,"Time Step")
        
        for key in state_d:
            sheet1.write(key+1, 0,"Node " + str(key))
            sheet1.write(0,key+1, key)
        return book,sheet1

    def writeExcel(self,sheet,x,n,state):
        sheet.write(x+1,n+1,state)

    def saveExcel(self,book):
        book.save("trial.xls")
            
    def endTest(self,state_d,i):
        print("Dictionary after ", i+1, "runs")
        print("--------------------------------")
        print(state_d)
        print("Number of zeros: ", self.getZeros(state_d))
        print("Number of ones: ", self.getOnes(state_d))
