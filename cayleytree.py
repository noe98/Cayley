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

from Cayley.abstractnetwork import *

class CayleyTree(AbstractNetwork):
    """Creates the Cayley Tree object. The class needs integer values
       for number of generations and links."""
    
    def __init__(self,generations,links): #constructor method with parameters
        """Creates a Cayley Tree with desired number of generations and
           links."""
        self.generations = generations #instance variables
        self.links = links
        self.keys = list(range(self.nodeNumber()))
        AbstractNetwork.__init__(self)
        self.autoCreate()
        #self.cayleyProtect()
        
    def __str__(self):
        """Creates a string representation of the Cayley Tree."""
        a = "Cayley Tree has " + str(self.generations) + " generations" + "\n"
        b = "Cayley Tree has " + str(self.links) + " links per node" + "\n"
        c = "Number of Nodes: " + str(self.nodeNumber()) + "\n"
        d = "Nodes per Generation: " + str(self.nodeGeneration())  + "\n"
        e = "Links of the Cayley Tree: " + str(self.link_d) 
        return a+b+c+d+e

    def __eq__(self,other):
        """Define equality of Cayley Tree objects, based on the idea that they
           must have same number of generations and links per node."""
        if self is other:
            return True
        if type(self) != type(other):
            return False
        elif self.links == other.links and self.generations == other.generations:
            return True
        else:
            return False

    def getType(self):
        """Just for quick fix in MonteCarlo."""
        return "CayleyTree"
            
    def cayleyProtect(self):
        """Protects the user from creating and using a Cayley Tree object that
           cannont exist."""
        if self.generations == 0 and self.links > 0:
            raise ValueError("Inappropriate argument value: Cayley Tree cannot \
                             exist")
        if self.links < self.generations:
            raise ValueError("Inappropriate argument value: Cayley Tree cannot \
                             exist")
        
    def nodeNumber(self):
        """Returns the total number of nodes in the Cayley tree. """
        return sum(self.nodeGeneration())

    def nodeGeneration(self):
        """Returns a list with the number of nodes per generation in the Cayley
           Tree."""
        list_of_nodes_by_generation = [1]
        for x in range(1,self.generations+1):
            nodes = (self.links * (self.links - 1)**(x - 1))
            list_of_nodes_by_generation.append(nodes)
        return list_of_nodes_by_generation

    def nodeCountGen(self,gen):
        """Takes a generation and returns the number of generations in the
           node."""
        return (self.links*(self.links - 1)**(gen - 1))

    def graphicsLinks(self): 
        """Returns a list of tuples that represents each link in the Cayley
           Tree. Only useful for CayleyGraphics class because of the Networkx
           package."""
        link_list = list()
        exclude = self.nodeGeneration()[-1]
        for x in range(1,self.links + 1):
            link_list.append((0,x))
        nodes_done = self.links + 1
        if nodes_done < self.nodeNumber():
            for x in range(1,self.nodeNumber() - exclude):
                for y in range(1,self.links):
                    link_list.append((x,nodes_done))
                    nodes_done += 1
        return link_list

    def autoCreate(self):
        """Creates a dictionary with the node number as the key and with a list of
           its neighbors as the value. This method will be used in MonteCarlo
           class, since this dictionary will reduce the runtime of its simulate
           method."""
        link_d = dict()
        node_gens = self.nodeGeneration()
        #sets up 0
        link_d[0] = set(range(1,self.nodeGeneration()[1]+1))
        node_count = self.nodeGeneration()[1]
        #goes up tree
        for node in range(1,self.nodeNumber()):
            if node_count + 1 != self.nodeNumber():
                link_d[node] = {node_count+x for x in range(1,self.links)}
                node_count += self.links-1
            else:
                link_d[node] = set()
        #goes down tree
        node_count = 0
        link_tally = 0
        for node in range(1,self.nodeNumber()):
            if node <= self.links:
                link_d[node] = link_d.get(node,set()).union({0})
                if node == self.links:
                    node_count += 1
            else:
                link_d[node] = link_d.get(node,set()).union({node_count})
                link_tally += 1 
                if link_tally == self.links - 1:
                    node_count += 1
                    link_tally = 0
        self.link_d = link_d
        return link_d
        
    def genFinder(self,node):
        """Takes a node and returns the generation that the node is in."""
        b = self.nodeGeneration()
        count_gen = -1
        for x in range(len(b)):
            node = node - b[x]
            count_gen += 1
            if node < 0:
                return count_gen

    def nodeFinder(self,gen):
        """Takes a generation and returns a list with the nodes in
            the generation."""
        b = self.nodeGeneration()
        a = sum(b[0:gen])
        c = self.nodeNumber()-sum(b[gen+1:self.generations+1])
        return list(range(a,c))

