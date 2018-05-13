"""
Authors: Justin Pusztay
Filename: lattice.py
Project: Research for Irina Mazilu, Ph.D.

This file contains the Lattice class. This class creates a Cayley Tree
object, by setting up the nodes and links between nodes. It also has methods
which allow for some basic analysis of the class such as number of nodes and
nodes per floor. 	
"""

from abstractnetwork import AbstractNetwork

class Lattice(AbstractNetwork):
    """Creates the Lattice object. The class needs integer values for the
    length, width, and height based on the number of nodes. It defaults to a
    2-demensional lattice."""

    def __init__(self,length,width,height = 1):
        """Sets up the demenstions of the lattice."""
        self.x = length
        self.y = width
        self.z = height-1
        self.latticeProtect()
        self.keys = list(range(self.nodeNumber()))
        AbstractNetwork.__init__(self)
        
    def __eq__(self,other):
        """Defines equality of a lattice based on the demensions."""
        if self is other:
            return True
        if type(self) != type(other):
            return False
        elif self.x == other.x and self.y == other.y and \
             self.z == other.z:
            return True
        else:
            return False

    def latticeProtect(self):
        """Protects the user from creating a lattice that cannot exist."""
        if self.y < 0 or self.x < 0 or self.z < 0:
            raise ValueError("Inappropriate entries lattice cannot \
                             exist")
    def nodeNumber(self):
        """Returns the total number of nodes in the Lattice."""
        if self.z <= 0:
            return self.x*self.y
        elif self.z == 1:
            return 2*self.x*self.y
        return (self.z+1)*self.y*self.x

    def floorArea(self):
        """Returns the number of nodes in a cross section of the z-plane."""
        return self.x*self.y

    def linkCreator(self):
        """Creates the links present in a lattice. Has a dictionary with the node
        number as the key and a list of neighbors as the value."""
        link_d = dict()
        #in x-direction
        for count in range(self.nodeNumber()):
            column_count = count % self.x
            if column_count % self.x != self.x -1: #checks if at x-max
                link_d[count] = [count+1]
            if column_count % self.x != 0: #checks if at x-min
                link_d[count] = link_d.get(count,list()) + [count-1]
        #in y-direction
        row_count = 0
        for count in range(self.nodeNumber()):
            if row_count % self.y != self.y-1: #checks if at y-max
                link_d[count] = link_d.get(count,list()) + [count+self.x]
            if row_count % self.y != 0: #checks if at y-min
                link_d[count] = link_d.get(count,list()) + [count - self.x]
            if count % self.x == self.x - 1:
                row_count += 1
        #in-z-dirction
        floor_count = 0
        for count in range(self.nodeNumber()):
            if floor_count != self.z: #checks if at z-max
                link_d[count] = link_d.get(count,list()) + [count+self.floorArea()]
            if floor_count != 0: #checks if at z-min
                link_d[count] = link_d.get(count,list()) + [count-self.floorArea()]
            if count % self.floorArea() == self.floorArea() - 1:
                floor_count += 1
        self.link_d = link_d
        return link_d

    def nearestNeighborFinder(self,node):
        """Finds the nodes that are neighbors to the node in question."""
        #return self.link_d[node]
        return self.linkCreator()[node]
