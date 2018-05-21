"""
Authors: Justin Pusztay
Filename: abstractnetwork.py
Project: Research for Irina Mazilu, Ph.D.

Contains the implentation of the abstract network.
"""

class AbstractNetwork(object):

    def __init__(self):
        self.link_d = dict()
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

    def degree(self,node):
        """Returns the degree of a node."""
        return len(self.link_d[node])

    def add(self,node):
        """Adds a node to graph."""
        self.link_d[node] = list()
        self.keys.append(node)

    def linkCreator(self,node,connection):
        """Adds a link in between two nodes."""
        if connection not in self.link_d:
            return NameError("Nde not found in graph")
        self.link_d[node] = self.link_d.get(node,list()) + [connection]
        self.link_d[connection] = self.link_d.get(connection,list()) + [node]

    def clear(self):
        self.link_d = dict()

    def nearestNeighborFinder(self,node):
        """Finds the neighbors between of the node."""
        return self.link_d[node] 
