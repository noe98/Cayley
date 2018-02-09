import networkx as nx
import matplotlib.pyplot as plt
from random import *
import xlwt
import math

class MonteCarlo(object):
    
    def __init__(self,dicty,alpha,beta,gamma,excel,graph):
        """Runs the Monte Carlo simulation the desired number of times."""
        #LOOK LATER AT TRANSITION RATE OVERTIME FOR NODE
        #Store previous and new previous in cache for staggered comparison (1)
        print("Initial Dictionary")
        print("--------------------")
        print(dicty)
        time_steps = range(len(dicty))
        if(excel):
            book = xlwt.Workbook(encoding="utf-8")
            sheet1 = book.add_sheet("Sheet 1")
            rows = list()
            cols = list()
            sheet1.write(0,0,"Time Step")
        
            for key in dicty:
                sheet1.write(key+1, 0,"Node " + str(key))
                sheet1.write(0,key+1, key)

        #HERE (1)
        for n in time_steps:
            for x in dicty:
                summ = self.NearestNeighborCalculator(x,dicty,graph)
        
                transition_rate_prob = gamma*dicty[x] + \
                                       (1 - dicty[x])*alpha*(beta**(summ))
                #print(transition_rate_prob)
                
                if uniform(0, 1) <= transition_rate_prob and dicty[x] == 0:
                    dicty[x] = 1
                    if(excel):
                        sheet1.write(x+1,n+1,dicty[x])
                    
                elif uniform(0, 1) <= transition_rate_prob and dicty[x] == 1:
                    dicty[x] = 0
                    if(excel):
                        sheet1.write(x+1,n+1,dicty[x])
                else:
                    if(excel):
                        sheet1.write(x+1,n+1,dicty[x])
            self.test(dicty,n)
        if(excel):
            book.save("trial.xls")
            
    def getZeros(self,dicty):
        return len(dicty) - sum(dicty.values())
    
    def getOnes(self,dicty):
        return sum(dicty.values())

    def NearestNeighborCalculator(self,node,dicty,graph):
        """Calculates the sum of the nearest neighbors for a node."""
        sum_of_neighbors = 0
        for node in self.NearestNeighborFinder(node,graph):
            sum_of_neighbors += dicty[node]
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
            
    def test(self,dicty,i):
        print("Dictionary after ", i+1, "runs")
        print("--------------------------------")
        print(dicty)
        print("Number of zeros: ", self.getZeros(dicty))
        print("Number of ones: ", self.getOnes(dicty))
