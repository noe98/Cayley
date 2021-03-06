"""
Authors: Justin Pusztay, Matt Lubas, and Griffin Noe
Filename: cayleytree.py
Project: Research for Irina Mazilu, Ph.D.

This file contains the CayleyTree class. This class creates a Cayley Tree
object, by setting up the nodes and links between nodes. It also has methods
which allow for some basic analysis of the class such as number of nodes
and nodes per generation. 
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)',
                        'Matt Lubas (lubasm18@mail.wlu.edu',
                        'Griffin Noe (noeg21@mail.wlu.edu'])

__all__ = ['CayleyTree']

from .abstractnetwork import AbstractNetwork

class CayleyTree(AbstractNetwork):
    """Creates the Cayley Tree object. The class needs integer values
       for number of generations and links."""
    
    def __init__(self,generations,links,names = None): 
        """Creates a Cayley Tree with desired number of generations and
           links."""
        AbstractNetwork.__init__(self)
        self.generations = generations
        self.links = links
        self.keys = list(range(len(self)))
        self.__names = names
        self._autoCreate()
        
    def getType(self):
        """Just for quick fix in MonteCarlo."""
        return "CayleyTree"

    def _nodeGeneration(self):
        """Returns a list with the number of nodes per generation in the Cayley
           Tree."""
        list_of_nodes_by_generation = [1]
        for x in range(1,self.generations+1):
            nodes = (self.links * (self.links - 1)**(x - 1))
            list_of_nodes_by_generation.append(nodes)
        return list_of_nodes_by_generation

    def _autoCreate(self):
        """Creates a dictionary with the node number as the key and with a list of
           its neighbors as the value. This method will be used in MonteCarlo
           class, since this dictionary will reduce the runtime of its simulate
           method."""
        try:
            for x in self.__names:
                self.add(x)
        except TypeError:
            for x in range(sum(self._nodeGeneration())):
                self.add(x)
        self.addMultipleEdges(self.nodes[0],{self.nodes[x] for x in
                                    range(1,self._nodeGeneration()[1]+1)})
        node_count = self._nodeGeneration()[1]
        for node in range(1,len(self)):
            if node_count + 1 != len(self):
                self.addMultipleEdges(self.nodes[node],
                                {self.nodes[node_count+x] for x in
                                 range(1,self.links)})
                node_count += self.links-1
        
    def genFinder(self,node):
        """Takes a node and returns the generation that the node is in."""
        b = self._nodeGeneration()
        count_gen = -1
        for x in range(len(b)):
            node = node - b[x]
            count_gen += 1
            if node < 0:
                return count_gen

    def nodesPerGen(self,gen):
        """Takes a generation and returns a list with the nodes in
            the generation."""
        b = self._nodeGeneration()
        a = sum(b[0:gen])
        c = len(self)-sum(b[gen+1:self.generations+1])
        return list(range(a,c))

