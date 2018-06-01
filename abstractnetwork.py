"""
Authors: Justin Pusztay
Filename: abstractnetwork.py
Project: Research for Irina Mazilu, Ph.D.

Contains the implentation of the abstract network.
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['AbstractNetwork']

import numpy as np

class AbstractNetwork(object):

    def __init__(self):
        """Sets up the link dictionary and the mod count."""
        self.link_d = dict()
        self._modCount = 0
        self.edge_list = None
        
    def __iter__(self):
        """Allows iteration over self."""
        temp = self._modCount
        cursor = 0
        while cursor < len(self):
            yield self.keys[cursor]
            if temp != self._modCount:
                raise AttributeError("Illegal modification of the backing store.")   
            cursor += 1

    def __len__(self):
        """Returns the number of nodes in the network."""
        return self.nodeNumber()

    def degree(self,node):
        """Returns the degree of a node."""
        return len(self.link_d[node])

    def add(self,node):
        """Adds a node to graph."""
        self.link_d[node] = set()
        self.keys.append(node)

    def linkCreator(self,node,connection):
        """Adds a link in between two nodes."""
        if connection not in self.link_d:
            return NameError("Nde not found in graph")
        (self.link_d[node]).add(connection)
        (self.link_d[connection]).add(node)
    
    def clear(self):
        """Clears the network of all links and nodes."""
        self.link_d = dict()
        self.edge_list = np.zeros([0,0],dtype=int)

    def nearestNeighborFinder(self,node):
        """Finds the neighbors between of the node."""
        return self.link_d[node]

    def edgeList(self):
        """Uses the link dictionary to create a numpy array that is the
        adjacency matrix for any network."""
        self.edge_list = np.zeros([len(self),len(self)], dtype = int)
        for node in self:
            for connection in self.link_d[node]:
                self.edge_list[node,connection] = 1
                self.edge_list[connection,node] = 1    
        return self.edge_list

    def linksAsTuples(self):
        """Returns a list of tuples that can represent each link in a
        network."""
        tuples = list()
        for x in self:
            edges = list(filter(lambda node: node[0] > x or \
                                                node[1] > x,
                                                list(map(lambda node:(x,node),
                                                         self.link_d[x]))))
            tuples = tuples + edges
        return tuples
