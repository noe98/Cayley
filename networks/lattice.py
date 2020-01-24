"""
Authors: Justin Pusztay
Filename: lattice.py
Project: Research for Irina Mazilu, Ph.D.

This file contains the Lattice class. This class creates a Cayley Tree
object, by setting up the nodes and links between nodes. It also has methods
which allow for some basic analysis of the object such as number of nodes and
nodes per floor.
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['Lattice']

from .abstractnetwork import AbstractNetwork
from math import floor

class Lattice(AbstractNetwork):
    """Creates the Lattice object. The class needs integer values for the
    length, width, and height based on the number of nodes. It defaults to a
    2-dimensional lattice."""

    def __init__(self,length,width,height = 1,names = None):
        """Sets up the dimensions of the lattice."""
        AbstractNetwork.__init__(self)
        self.x = length
        self.y = width
        self.z = height
        self.__names = names
        self.latticeProtect()
        self.keys = list(range(self.nodeNumber()))
        self.autoCreate()

    def __eq__(self,other):
        """Defines equality of a lattice based on the dimensions."""
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
        if self.y <= 0 or self.x <= 0 or self.z <= 0:
            raise ValueError("Inappropriate entries lattice cannot \
                             exist")
    def nodeNumber(self):
        """Returns the total number of nodes in the Lattice."""
        return self.z*self.y*self.x

    def getType(self):
        """Quick fix for MonteCarlo"""
        return "Lattice"

    def floorArea(self):
        """Returns the number of nodes in a cross section of the z-plane."""
        return self.x*self.y

    def autoCreate(self):
        """Creates the links present in a lattice. If the object was created
        with a given set of names that go in the order that the lattice is
        numbered, then the nodes will be properly linked as intended.

        If no names are given, it just uses a number as a name."""
        try:
            for x in self.__names:
                self.add(x)
        except TypeError:
            for x in range(self.nodeNumber()):
                self.add(x)
        row_count = 0 #x-coordinate
        floor_count = 0 #z-coordinate
        node_count = 0
        for node in self:
            column_count = node_count % self.x #x-coordinate
            row_count = floor(node_count/self.x) % self.y
            floor_count = floor(node_count/(self.x*self.y))
            self.add(node,coords = (column_count,row_count,floor_count))
            #above adds coordinate as feature
            if column_count % self.x != self.x -1: #checks if at x-max
                self.addEdge(node,self.nodes[node_count+1])
            if column_count % self.x != 0: #checks if at x-min
                self.addEdge(node,self.nodes[node_count-1])
            if row_count % self.y != self.y-1: #checks if at y-max
                self.addEdge(node,self.nodes[node_count+self.x])
            if row_count % self.y != 0: #checks if at y-min
                self.addEdge(node,self.nodes[node_count-self.x])
            if floor_count != self.z-1: #checks if at z-max
                self.addEdge(node,self.nodes[node_count+self.floorArea()])
            if floor_count != 0: #checks if at z-min
                self.addEdge(node,self.nodes[node_count-self.floorArea()])
            node_count += 1
            
