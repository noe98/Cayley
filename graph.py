"""
Authors: Justin Pusztay
Filename: graph.py
Project: Research for Irina Mazilu, Ph.D.

This file contains the graph class. Allows users to build their own graph.
"""

from abstractnetwork import AbstractNetwork

class Graph(AbstractNetwork):

    def __init__(self):
        """Creates the graph object."""
        self.keys = list()
        AbstractNetwork.__init__(self)
         
    def __eq__(self,other):
        """Need to look at Lambert's."""
        if self is other:
            return True
        if type(self) != type(other):
            return False

    def nodeNumber(self):
        """Returns the total number of nodes in the Lattice."""
        return len(self.link_d)

    def add(self,node):
        """Adds a node to graph."""
        self.link_d[node] = list()
        self.keys.append(node)
    
    def linkCreator(self,node,connection):
        """Adds a link in between two nodes."""
        if connection not in self.link_d:
            return NameError("Node not found in graph")
        self.link_d[node] = self.link_d.get(node,list()) + [connection]
        self.link_d[connection] = self.link_d.get(connection,list()) + [node]

    def nearestNeighborFinder(self,node):
        """Finds the neighbors between of the node."""
        return self.link_d[node]        
