"""
Authors: Justin Pusztay
Filename: lattice.py
Project: Research for Irina Mazilu, Ph.D.

This file contains the Lattice class. This class creates a Cayley Tree
object, by setting up the nodes and links between nodes. It also has methods
which allow for some basic analysis of the class such as number of nodes and
nodes per floor. 	
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['Lattice']

from Cayley.abstractnetwork import *

class Lattice(AbstractNetwork):
    """Creates the Lattice object. The class needs integer values for the
    length, width, and height based on the number of nodes. It defaults to a
    2-demensional lattice."""

    def __init__(self,length,width,height = 1,names = None):
        """Sets up the demenstions of the lattice."""
        self.x = length
        self.y = width
        self.z = height-1
        self.__names = names
        self.latticeProtect()
        self.keys = list(range(self.nodeNumber()))
        AbstractNetwork.__init__(self)
        self.autoCreate()
        
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

    def getType(self):
        """Quick fix for MonteCarlo"""
        return "Lattice"

    def floorArea(self):
        """Returns the number of nodes in a cross section of the z-plane."""
        return self.x*self.y

    def autoCreate(self):
        """Creates the links present in a lattice. Has a dictionary with the
        node number as the key and a list of neighbors as the value."""
        try:
            for x in self.__names:
                self.add(x)
        except TypeError:
            for x in self:
                self.add(x)
            row_count = 0
            floor_count = 0
            for node in self:
                column_count = node % self.x
                if column_count % self.x != self.x -1: #checks if at x-max
                    self.linkCreator(node,node+1)
                if column_count % self.x != 0: #checks if at x-min
                   self.linkCreator(node,node-1)
                   
                if row_count % self.y != self.y-1: #checks if at y-max
                    self.linkCreator(node,node+self.x)
                if row_count % self.y != 0: #checks if at y-min
                    self.linkCreator(node,node-self.x)
                if node % self.x == self.x - 1:
                    row_count += 1
        
                if floor_count != self.z: #checks if at z-max
                    self.linkCreator(node,node+self.floorArea())
                if floor_count != 0: #checks if at z-min
                    self.linkCreator(node,node-self.floorArea())
                if node % self.floorArea() == self.floorArea() - 1:
                    floor_count += 1
 
