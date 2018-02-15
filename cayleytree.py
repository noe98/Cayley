"""
Authors: Justin Pusztay, Matt Lubas, and Griffin Noe
Filename: cayleytree.py

This file contains the CayleyTree class. This class creates a Cayley Tree
object, by setting up the nodes and links between nodes. It also has methods
which allow for some basic analysis of the class such as number of nodes
and nodes per generation. 
"""


class CayleyTree(object):
    """Creates the Cayley Tree object. The class needs integer values
       for number of generations and links."""
    
    def __init__(self,generations,links):
        """Creates a Cayley Tree with desired number of generations and
           links."""
        self.generations = generations
        self.links = links
        self.linkCreator()

    def __str__(self):
        """Creates a string representation of the Cayley Tree."""
        a = "Cayley Tree has " + str(self.generations) + " generations" + "\n"
        b = "Cayley Tree has " + str(self.links) + " links per node" + "\n"
        c = "Number of Nodes: " + str(self.nodeNumber()) + "\n"
        d = "Nodes per Generation: " + str(self.nodeGeneration())  + "\n"
        e = "Links of the Cayley Tree: " + str(self.linkCreator()) 
        return a+b+c+d+e

    def nodeNumber(self):
        """Returns the total number of nodes in the Cayley tree. """
        number_nodes = 1
        for x in range(1,self.generations+1):
            number_nodes += (self.links * (self.links - 1)**(x - 1))
        return number_nodes

    def nodeGeneration(self):
        """Returns a list with the number of nodes per generation in the Cayley
           Tree."""
        list_of_nodes_by_generation = [1]
        for x in range(1,self.generations+1):
            nodes = (self.links * (self.links - 1)**(x - 1))
            list_of_nodes_by_generation.append(nodes)
        return list_of_nodes_by_generation

    def linkCreator(self): 
        """Returns a list of tuples that represents each link in the Cayley
           Tree."""
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
        
