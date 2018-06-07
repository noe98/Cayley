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
        self.graph = dict()
        self._modCount = 0
        
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

    def __str__(self):
        return str(self.graph)

    def degree(self,node):
        """Returns the degree of a node."""
        return len(self.graph[node]["Neighbors"])

    def add(self,node):
        """Adds a node to graph."""
        self.graph[node] = dict()
        self.keys.append(node)
        self.graph[node]["Neighbors"] = set()

    def setNodeFeature(self,name,value = None):
        for x in self:
            self.graph[x][name] = value

    def getNodeFeature(self,name):
        return {n: self.graph[n][name] for n in self if name in self.graph[n]}
            
    def linkCreator(self,node,connection):
        """Adds a link in between two nodes."""
        try:
            (self.graph[node]["Neighbors"]).add(connection)
            (self.graph[connection]["Neighbors"]).add(node)
        except KeyError:
            return "Nodes not in graph"
        
    def clear(self):
        """Clears the network of all links, nodes, and data."""
        self.graph = dict()
        self.edge_list = np.zeros([0,0],dtype=int)

    def neighborFinder(self,node):
        """Finds the neighbors between of the node."""
        return self.graph[node]["Neighbors"]

    def edgeList(self):
        """Uses the link dictionary to create a numpy array that is the
        adjacency matrix for any network."""
        edge_list = np.zeros([len(self),len(self)], dtype = int)
        for node in self:
            for connection in self.graph[node]["Neighbors"]:
                edge_list[node,connection] = 1
                edge_list[connection,node] = 1    
        return edge_list

    def linksAsTuples(self):
        """Returns a list of tuples that can represent each link in a
        network."""
        tuples = list()
        for x in self:
            edges = list(filter(lambda node: node[0] > x or \
                                node[1] > x,
                                    list(
                                        map(lambda node:(x,node),
                                            self.graph[x]["Neighbors"]))))
            tuples = tuples + edges
        return tuples
