"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe
Filename: latticegraphics.py
Project: Research for Irina Mazilu, Ph.D.

Contains the class LatticeGraphics, which generates a GUI image of the
Lattice Graph. 

Code Adapted from: https://www.udacity.com/wiki/creating-network-graphs-with-python

USE THIS LINK JUSTIN!
https://networkx.github.io/documentation/networkx-1.9.1/reference/classes.graph.html#iterating-over-nodes-and-edges
"""

import networkx as nx
import matplotlib.pyplot as plt



class LatticeGraphics(object):
    
    def __init__(self):
            """Creates a CayleyTree object in order to create an image
               of the graph."""
            self.GraphList = []            
            #self.tree = LatticeGraphics(length, width, height)

    def drawLattice(self,labels=None, graph_layout='spring',
                       node_size=1000, node_color='blue', node_alpha=0.3,
                       node_text_size=12,
                       edge_color='blue', edge_alpha=0.3, edge_thickness=2,
                       edge_text_pos=0.3,
                       text_font='sans-serif'):
            """Method that physically draws the lattice graph based on length,
            width, and height."""

            
            l = int( input("What is the length of the lattice?"))
            w = int( input("What is the width of the lattice?"))
            h = int( input("What is the height of the lattice?"))
                                
            
            graph=nx.grid_graph([l,w,h])

            
            # add edges
            for edge in self.GraphList:
                graph.add_edge(edge[0], edge[1])

            # these are different layouts for the network you may try
            # shell seems to work best
            if graph_layout == 'spring':
                graph_pos=nx.spring_layout(graph)
            elif graph_layout == 'spectral':
                graph_pos=nx.spectral_layout(graph)
            elif graph_layout == 'random':
                graph_pos=nx.random_layout(graph)
            else:
                graph_pos=nx.shell_layout(graph)

            # draw graph
            nx.draw_networkx_nodes(graph,graph_pos,node_size=node_size, 
                                   alpha=node_alpha, node_color=node_color)
            nx.draw_networkx_edges(graph,graph_pos,width=edge_thickness,
                                   alpha=edge_alpha,edge_color=edge_color)
            nx.draw_networkx_labels(graph, graph_pos,font_size=node_text_size,
                                    font_family=text_font)

            if labels is None:
                labels = range(len(graph))

            edge_labels = dict(zip(graph, labels))

            #Nodes prints the coordinates of the node positions
            #n = nx.nodes(graph)
            #print(n)

            #Number of Nodes is helpful
            nn = nx.number_of_nodes(graph)
            print(nn)

            #Prints <dict_keyiterator object at 0x116fd3318>
            neighbors = nx.all_neighbors(graph, (0,0,1))
            print(neighbors)
            
            #e = nx.edges(graph)
            #print(e)
            
            # show graph
            plt.show()
                    

#LatticeGraphics.drawLattice(GraphList)

