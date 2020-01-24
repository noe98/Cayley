"""
Authors: Justin Pusztay
Filename: graph.py
Project: Research for Irina Mazilu, Ph.D.

This file contains the graph class. Allows users to build their own graph.
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['Graph']

from .abstractnetwork import AbstractNetwork

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
        return len(self.graph)

    def getType(self):
        """Quick fix for MonteCarlo."""
        return "Graph"

       
