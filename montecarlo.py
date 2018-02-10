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
        lyst = self.simulate(state_d,alpha,beta,gamma,graph)
        if(excel):
            for n in range(len(lyst)):
                for x in range(len(lyst[n])):
                    self.writeExcel(sheet,x,n,lyst[n][x])
            self.saveExcel(book)
##            self.endTest(state_d,n)

    def simulate(self, _dict,a,b,g,graph):
        time_steps = range(len(_dict))
        list_cache = list()
        list_cache.append(_dict)
        for n in time_steps:
            cache = dict()
            for x in range(len(_dict)):
                summ = self.NearestNeighborCalculator(x,list_cache[n],graph)
##                print("summ: ", summ)
                transition_rate_prob = g*list_cache[n][x] + \
                                       (1 - list_cache[n][x])*a*(b**(summ))
                if uniform(0, 1) <= transition_rate_prob and list_cache[n][x] == 0:
                    cache[x] = 1 #uniform is from random library
                elif uniform(0, 1) <= transition_rate_prob and \
                     list_cache[n][x] == 1:
                    cache[x] = 0 #uniform is from random library
                else:
                    cache[x] = list_cache[n][x]
                
##                print("cache: ",cache)
            list_cache.append(cache)
        return list_cache
##            print("Previous cache: ", list_cache[n])

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
