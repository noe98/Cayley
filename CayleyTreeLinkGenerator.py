#!/usr/bin/env python
"""
Author: Justin Pusztay and Matt Lubas

This is a program that is TUI for a Cayley Tree tuple generator. It will request
the input of number of connections per node and the number of generations.

Code Adapted from: https://www.udacity.com/wiki/creating-network-graphs-with-python

"""

import networkx as nx
import matplotlib.pyplot as plt
from random import *
import csv

gamma = .1
beta = .2
alpha = .5

graph = list()
node_dict = dict()
generations = int(input("What is the number of generations? "))
connections = int(input("What is the number of connections? "))

def draw_graph(graph, labels=None, graph_layout='spring',
               node_size=1000, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=2,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    #creates a Cayley-like tree with links and connections
    #G =nx.balanced_tree(connections,generations)

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

def NodesPerGeneration(generations, connections):
    """This functions takes the number of generations and connections and
       returns a list of nodes per generation."""
    lyst_of_nodes_by_generation = [1]
    for x in range(1,generations+1):
        nodes = (connections * (connections - 1)**(x - 1))
        lyst_of_nodes_by_generation.append(nodes)
    return lyst_of_nodes_by_generation

def NodeCalculator(generations, connections):
    """This functions takes in number of generations and connections and
       returns the number of nodes in the graph."""
    number_nodes = 1
    for x in range(1,generations+1):
        number_nodes += (connections * (connections - 1)**(x - 1))
    return number_nodes

def TupleOrganizer(generations, connections): #RENAME TO GRAPH CREATOR or something
    """This function generates the tuples for the Cayley Tree."""
    nodes = NodeCalculator(generations, connections)
    NodesPerGeneration(generations, connections)
    exclude = NodesPerGeneration(generations, connections)[-1]
    for x in range(1,connections+1): #sets up 0 
        graph.append((0,x))
    nodes_done = connections + 1
    if nodes_done < nodes:
        for x in range(1,nodes-exclude):
            for y in range(1,connections):
                graph.append((x,nodes_done))
                nodes_done += 1

def initiateNodeDictionary():
    """Creates an initial dictioary with nodes as integer types in the key and
       assigns a 0 to represent the unfilled state as the value.
       The key in dictionary is node, the value is the state."""
    for x in range(NodeCalculator(generations,connections)):
        node_dict[x] = 0
    return node_dict

def NearestNeighborFinder(node):
    """Finds the nodes that are neighbors to the node in question."""
    neighbors = list(filter(lambda x: x.count(node) > 0, graph))
    neighbors_list = list()
    for x in neighbors:
        if x[0] != node:
            neighbors_list.append(x[0])
        elif x[1] != node: 
            neighbors_list.append(x[1])
    return neighbors_list

def NearestNeighborCalculator(node):
    """Calculates the sum of the nearest neighbors for a node."""
    sum_of_neighbors = 0
    for node in NearestNeighborFinder(node):
        sum_of_neighbors += node_dict[node]
    return sum_of_neighbors

def random_node_selector():
    """Selecting the nodes randomly out of given total generations and edges."""
    list_nodes = list(range(NodeCalculator(generations,connections)))
    shuffle(list_nodes)
    #print(list_nodes)
    for x in list_nodes:
        summ = NearestNeighborCalculator(x)
        transition_rate_prob = gamma*node_dict[x] + (1 - node_dict[x])*alpha*(beta**(summ))
        print(transition_rate_prob)
##        rand_value = randint(0,2)
##        node_dict[x] = rand_value
##    return node_dict

def monteCarlo():
    """Runs the Monte Carlo simulation the desired number of times."""
    for x in range(NodeCalculator(generations,connections)):
        random_node_selector()
        sum_of_zeros = 0
        sum_of_ones = 0
        sum_of_twos = 0
        for state in node_dict.values():
            if state == 0:
                sum_of_zeros += 1
            elif state == 1:
                sum_of_ones += 1
            else:
                sum_of_twos += 1
        #print("Round " + str(x))
        #print("Number of zeros: ", sum_of_zeros)
        #print("Number of ones: ", sum_of_ones)
        #print("Number of twos: ", sum_of_twos)

def CreateCSVfile():
    with open('test.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerows(graph)


def main():
    print("The number of nodes is: ",NodeCalculator(generations, connections))
    print("Nodes per generations is: ", NodesPerGeneration(generations, connections))
    TupleOrganizer(generations, connections) #generates graph
    print(graph) #prints list of connecttions generated in TupleOrganizer
    draw_graph(graph) #Creates plot of Cayley Tree
    initiateNodeDictionary() #creates inital state of dictionary
    random_node_selector() #does 1 step of Monte Carlo with transtion rate
    print("Nearest Neighbor Sum: ", NearestNeighborCalculator(8))
    print(NearestNeighborFinder(8)) #prints list with nearest neighbors
    print(NearestNeighborFinder(3))
    monteCarlo() #runs Monte Carlo n-times
    #CreateCSVfile()

if __name__ == "__main__":
    main()
