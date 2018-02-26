"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe
Filename: cayleygraphics.py

Contains the class cayleygraphics, which generates a GUI image of the
Cayley Tree. 

Code Adapted from: https://www.udacity.com/wiki/creating-network-graphs-with-python
"""

import networkx as nx
import matplotlib.pyplot as plt
from cayleytree import CayleyTree

class CayleyGraphics(object):

    def __init__(self,generations,links):
        """Creates a CayleyTree object in order to create an image
           of the graph."""
        
        self.tree = CayleyTree(generations, links)

    def drawGraph(self,labels=None, graph_layout='spring',
                   node_size=1000, node_color='cyan', node_alpha=0.3,
                   node_text_size=12,
                   edge_color='blue', edge_alpha=0.3, edge_thickness=2,
                   edge_text_pos=0.3,
                   text_font='sans-serif'):
        """Method that physically draws the graph based on generations
           and connections"""
        # create networkx graph
        G=nx.Graph()

        #creates a Cayley-like tree with links and connections
        #G =nx.balanced_tree(connections,generations)

        # add edges
        for edge in self.tree.linkCreator():
            G.add_edge(edge[0], edge[1])

        # these are different layouts for the network you may try
        # shell seems to work best
        if graph_layout == 'spring':
            graph_pos=nx.spring_layout(G)
        elif graph_layout == 'spectral':
            graph_pos=nx.spectral_layout(G)
        elif graph_layout == 'random':
            graph_pos=nx.random_layout(G)
        else:
            graph_pos=nx.shell_layout(G)

        # draw graph
        nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                               alpha=node_alpha, node_color=node_color)
        nx.draw_networkx_edges(G,graph_pos,width=edge_thickness,
                               alpha=edge_alpha,edge_color=edge_color)
        nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                                font_family=text_font)

        if labels is None:
            labels = range(len(self.tree.linkCreator()))

        edge_labels = dict(zip(self.tree.linkCreator(), labels))
        """
        #Below on how to label edges.
        nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                     label_pos=edge_text_pos)
        """
        # show graph
        plt.show()
