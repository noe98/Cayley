import networkx as nx
import matplotlib.pyplot as plt
from random import *
import xlwt
import math

class MonteCarlo(object):
    
    def __init__(self,state_d,alpha,beta,gamma,excel,graph):
        """Runs the Monte Carlo simulation the desired number of times."""
##        self.startTest(state_d)
        if(excel):
            book,sheet = self.makeExcel(state_d)
        self.simulate(state_d,alpha,beta,gamma,graph)
        if(excel):
            for n in range(len(state_d)):
                for x in range(len(state_d)):
                    self.writeExcel(sheet,x,n)
##            self.endTest(state_d,n)
        if(excel):
            self.saveExcel(book)

    def simulate(self, _dict,a,b,g,graph):
        time_steps = range(len(_dict))
        for n in time_steps:

            neighbor_state_cache = _dict
            for x in neighbor_state_cache:
                summ = self.NearestNeighborCalculator(x,_dict,graph)
        
                transition_rate_prob = g*_dict[x] + \
                                       (1 - _dict[x])*a*(b**(summ))
                
                if uniform(0, 1) <= transition_rate_prob and _dict[x] == 0:
                    _dict[x] = 1
                elif uniform(0, 1) <= transition_rate_prob and _dict[x] == 1:
                    _dict[x] = 0
##            self.writeExcel(sheet,x,n,state_d[x])
                            
    def getZeros(self,state_dict):
        return len(state_dict) - sum(state_dict.values())
    
    def getOnes(self,state_dict):
        return sum(state_dict.values())

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

    def startTest(self,state_d):
        print("Initial Dictionary")
        print("--------------------")
        print(state_d)
        
    def endTest(self,state_d,i):
        print("Dictionary after ", i+1, "runs")
        print("--------------------------------")
        print(state_d)
        print("Number of zeros: ", self.getZeros(state_d))
        print("Number of ones: ", self.getOnes(state_d))
