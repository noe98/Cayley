"""
Code Adapted from: https://www.udacity.com/wiki/creating-network-graphs-with-python

"""

import networkx as nx
import matplotlib.pyplot as plt
from random import *

def define_graph(number_of_nodes):
    graph2 = []
    for x in range(0, number_of_nodes):
        graph.append((x,x))
    return graph2
    

def draw_graph(graph, labels=None, graph_layout='spring',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
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
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    """
    #Below on how to label edges.
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)
    """
    # show graph
    plt.show()

graph = [(0, 1), (0, 2), (0,3), (1,4), (1,5),
         (1,6), (2, 7), (2, 8), (2, 9), (3,10), (3,11),(3,12)]

graph_gen = []
def gen_cayley_tree(generations, connections):
    """gen_cayley_tree creates a cayley tree like list using the inputed number
    of generations and connections per generations"""
    
    current_num=0
    for x in range(0,connections+1):
        graph_gen.append((0,x))
        current_num += 1
        
    print (current_num)


gen_cayley_tree(1,2)
"""

# n is the number of additional edges desired
"""
for x in range(0,2):
    graph.append((randint(0,15),randint(0,15)))
    print(graph,"\n")
"""
# you may name your edge labels
#labels = map(chr, range(65, 65+len(graph)))
#draw_graph(graph, labels)
#while input != "end":



# if edge labels is not specified, numeric labels (0, 1, 2...) will be used
draw_graph(graph)
