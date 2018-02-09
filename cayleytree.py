import networkx as nx
import matplotlib.pyplot as plt
from random import *
import xlwt
import math

class CayleyTree(object):
    """Creates the Cayley Tree object. The class needs integer values
       for number of generations and links."""
    
    def __init__(self,generations,links):
        """Initializes an empty list reserved for the tuples
           representing each link, a dictionary for nodes and their states,
           and the constants: alpha, gamma, and beta in the transition rate."""
        self.generations = generations
        self.links = links
        self.link_list = list()
        self.node_state_dict = dict()
        self.gamma = .1
        self.beta = .2
        self.alpha = .5

    def changeGamma(self,newGamma):
        """Changes the value of gamma from the default value
           of 0.1. Must input a float between 0 and 1."""
        self.gamma = newGamma
        
    def changeBeta(self,newBeta):
        """Changes the value of beta from the default value
           of 0.2. Must input a float between 0 and 1."""
        self.beta = newBeta

    def changeAlpha(self,newAlpha):
        """Changes the value of beta from the default value
           of 0.5. Must input a float between 0 and 1."""
        self.alpha = newAlpha

    def nodeCalculator(self):
        """Calculates the total number of nodes with a Cayley Tree and the
           list of nodes per generation. Returns those two data types as a
           tuple."""
        list_of_nodes_by_generation = [1]
        for x in range(1,self.generations+1):
            nodes = (self.links * (self.links - 1)**(x - 1))
            list_of_nodes_by_generation.append(nodes)
        return (sum(list_of_nodes_by_generation),list_of_nodes_by_generation)

    def linkCreator(self): 
        """Generates the tuples that represents each link in the Cayley Tree
           graph. It appends each tuple to the link_list list that is iniitiated
           when the Cayley Tree object is created."""
        self.nodeCalculator()
        exclude = self.nodeCalculator()[1][-1]
        for x in range(1,self.links + 1):
            self.link_list.append((0,x))
        nodes_done = self.links + 1
        if nodes_done < self.nodeCalculator()[0]:
            for x in range(1,self.nodeCalculator()[0] - exclude):
                for y in range(1,self.links):
                    self.link_list.append((x,nodes_done))
                    nodes_done += 1
        
