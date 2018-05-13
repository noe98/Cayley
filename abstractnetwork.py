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

    def getModCount(self):
        """Returns the number of mutations to this collection."""
        return self._modCount

    def incModCount(self):
        """Increments the number of mutations by one."""
        self._modCount += 1

    def resetSizeAndModCount(self):
        """Resets the numbers of items and mutations to 0."""
        self._size = 0
        self._modCount = 0
