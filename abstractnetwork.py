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
        self.nodes = list()
        self.graph = dict()
        self._modCount = 0
        
    def __iter__(self):
        """Allows iteration over self."""
        temp = self._modCount
        cursor = 0
        while cursor < len(self.nodes):
            yield self.nodes[cursor]
            if temp != self._modCount:
                raise AttributeError("Illegal modification of the backing store.")   
            cursor += 1

    def __len__(self):
        """Returns the number of nodes in the network."""
        return len(self.nodes)
    
    def __str__(self):
        return str(self.graph)

    def degree(self,node):
        """Returns the degree of a node."""
        return len(self.graph[node]["neighbors"])

    def add(self,node,**kwargs):
        """Adds a node to graph. Also adds a feature to a node. Can be a new
        feature or updates an old one."""
        if node not in self.graph: #handles adding a new node with new features
            self.graph[node] = dict()
            self.keys.append(node)
            self.graph[node] = kwargs
            self.graph[node]["neighbors"] = set()
            self.nodes.append(node)
        else: #if node is already in graph, handles updating features.
            for key in kwargs.items():
                try:
                    if key[1] != self.graph[node][key[0]]: #handles update
                        self.graph[node][key[0]] = key[1]
                except KeyError:
                    self.graph[node][key[0]] = key[1] #handles new feature to
                                                      #node that exits.
    def addMultipleNodes(self,nodes,**kwargs):
        try:
            for node in nodes:
                self.add(node,**kwargs)
        except TypeError:
            return "Nodes object is not iterable"

    def setNodeFeature(self,name,data): #broken, works weird and should have
        #**kwargs
        """Applies new feature or updates feature for all nodes in
        graph."""
        try:
            for node,datum in zip(self,data.items()):
                self.add(node,state = datum[1])
        except AttributeError:
            
            for node in self:
                a = name
                self.add(node,a = data)

    def getNodeFeature(self,name):
        return {n: self.graph[n][name] for n in self if name in self.graph[n]}

    def remove(self,node):
        """Does not remove links."""
        copy = self.graph
        del copy[node]
        self.graph = copy
        return self.graph
            
    def linkCreator(self,node,connection):
        """Adds a link in between two nodes."""
        try:
            (self.graph[node]["neighbors"]).add(connection)
            (self.graph[connection]["neighbors"]).add(node)
        except KeyError:
            return "Nodes not in graph"

    def multipleLinkCreator(self,node,connections):
        try:
            for connection in connections:
                (self.graph[node]["neighbors"]).add(connection)
                (self.graph[connection]["neighbors"]).add(node)
        except TypeError:
            return "Connections object is not iterable"
        
    def clear(self):
        """Clears the network of all links, nodes, and data."""
        self.graph = dict()
        self.edge_list = np.zeros([0,0],dtype=int)

    def neighborFinder(self,node):
        """Finds the neighbors between of the node."""
        return self.graph[node]["neighbors"]

    def edgeList(self):
        """Uses the link dictionary to create a numpy array that is the
        adjacency matrix for any network."""
        edge_list = np.zeros([len(self),len(self)], dtype = int)
        for node in self:
            for connection in self.graph[node]["neighbors"]:
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
                                            self.graph[x]["neighbors"]))))
            tuples = tuples + edges
        return tuples
