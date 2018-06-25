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

from Cayley.abstractnetwork import *
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
            node_count = 0
            for n in self.__names: ### WARNING: HAS NOT BEEN TESTED ###
                x = node_count%self.x
                y = floor(node_count/self.x)%self.y
                z = floor(node_count/(self.x*self.y))
                edge = (0 in [x,y,z] or x == self.x-1 \
                       or y == self.y-1 or z == self.z-1)
                self.add(n, coords = [x,y,z], edge_yes = edge)
                node_count += 1
        except TypeError:
            for n in range(self.nodeNumber()):
                x = n%self.x
                y = floor(n/self.x)%self.y
                z = floor(n/(self.x*self.y))
                edge = 0 in [x,y,z] or x == self.x-1 \
                       or y == self.y-1 or z == self.z-1
                self.add(n, coords = [x,y,z], edge_yes = edge)

        coor_d = self.getNodeFeature('coords')
        edges = self.getNodeFeature('edge_yes')
        node_count = 0
        for node in self: ### CAN THIS BE IMPROVED? ###
            if edges[node] == False:
                neighs = [node+1,node-1,node+self.x,node-self.x,\
                          node+self.floorArea(),node-self.floorArea()]
                self.multipleLinkCreator(node,neighs)
            else:
                c = coor_d[node]
                if c[0] != self.x -1: #checks if at x-max
                    self.linkCreator(node,self.nodes[node_count+1])
                if c[0] != 0: #checks if at x-min
                   self.linkCreator(node,self.nodes[node_count-1])

                if c[1] != self.y-1: #checks if at y-max
                    self.linkCreator(node,self.nodes[node_count+self.x])
                if c[1] != 0: #checks if at y-min
                    self.linkCreator(node,self.nodes[node_count-self.x])


                if c[2] != self.z-1 : #checks if at z-max
                    self.linkCreator(node,self.nodes[node_count+self.floorArea()])
                if c[2] != 0: #checks if at z-min
                    self.linkCreator(node,self.nodes[node_count-self.floorArea()])
            node_count += 1
        neigh_d = self.getNodeFeature('neighbors')
        edge_d = self.getNodeFeature('edge_yes')
        for node in self:
            if (edge_d[node]) and len(neigh_d[node]) == 6:
                print("Neighbor error: " + str(node))
            if (not edge_d[node]) and len(neigh_d[node]) != 6:
                print("Neighbor error: " + str(node))
