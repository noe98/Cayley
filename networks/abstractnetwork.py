"""
Authors: Justin Pusztay
Filename: abstractnetwork.py
Project: Research for Irina Mazilu, Ph.D.

Abstraction of all graphs created. These are methods that can be
implemented across many different graph objects. Examples included
Cayley Tree and Lattice. 
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['AbstractNetwork']

import numpy as np

class AbstractNetwork(object):
    """
    Abstract representation of all network objects. Both directed and undirected
    graphs can be used.

    All networks can store nodes and edges. Nodes can be any hashable object,
    and can hold many different types of data, which are called features.

    Name of data held by a node must be a hashable object with an optional
    key/value atribute.

    By convention, if feature names are strings they must in all lowercase
    characters. 

    *Features*

    Each node can hold multiple key/value pairs, where all keys must be
    hasable. These features can be added in the following way: using add,
    addMultipleNodes, and setFeature. If the node does not exist, the
    methods will add the node to the network. If the node exists, it will
    simply add the feature to the node. setFeature is used when adding a
    dictionary that has the nodes as keys and desired data as values.

    The only built in feature for all networks is the 'neighbors' feature,
    since links are a fundamental part of graphs. 

    The network is represented as a dictionary of dictionary implemenation.

    *Subclasses*

    More specific types of networks are subclasses. These in include Cayley
    Tree, Lattice, and Graph. 
    """

    def __init__(self):
        """
        Initializes an empty network. 
        """
        self.nodes = list()
        self.graph = dict()
        self._modCount = 0

    def __iter__(self):
        """
        Iterates over the nodes.
        """
        temp = self._modCount
        cursor = 0
        while cursor < len(self.nodes):
            yield self.nodes[cursor]
            if temp != self._modCount:
                raise AttributeError("Illegal modification of the backing store.")
            cursor += 1

    def __len__(self):
        """Returns the number of nodes in the network."""
        return len(self.nodes)

    def __str__(self):
        """Returns the string representation of the dictionary of dictionary."""
        return str(self.graph)

    def __contains__(self,node):
        """
        Return True if node is in network, False otherwise.

        Use 'node in network'. 

        The contains method as a runtime of $O(k)$ since dictionaries are
        being used.
        """
        try:
            return node in self.graph
        except TypeError:
            return False

    def __getitem__(self,node):
        """
        Returns a dictionary with all the node features for the node.

        Use network[node].

        Has a runtime of $O(k)$ since dictionaries are being used.
        """
        return self.graph[node]

    def getNodes(self):
        """Returns the list of nodes in the network."""
        return self.nodes

    def degree(self,node):
        """Returns the degree of a node."""
        return len(self.graph[node]["neighbors"])

    def add(self,node,**kwargs):
        """
        Adds an individual node to the graph with any features. It can also
        add new features and update existing ones.

        Parameters
        ----------
        node: node
           Can be any hashable Python object
        kwargs: keyword arguments, optional
           Can set features for a node by using key=value.

        The runtime is $O(k)$ when adding a new node. However, it can degrade
        to $O(n)$ when updating features or adding new features to an existing
        node.

        This also adds a new node to the node list.
        """
        if node not in self.graph: #handles adding a new node with new features
            self.graph[node] = dict()
            self.keys.append(node)
            self.graph[node] = kwargs
            self.graph[node]["neighbors"] = set()
            self.nodes.append(node)
        else: #if node is already in graph, handles updating features.
            for key in kwargs.items():
                try:
                    if key[1] != self.graph[node][key[0]]: #handles update
                        self.graph[node][key[0]] = key[1]
                except KeyError:
                    self.graph[node][key[0]] = key[1] #handles new feature to
                                                      #node that exits.
    def addMultipleNodes(self,nodes,**kwargs):
        """
        Adds multiple nodes to a network.

        Parameters
        ----------
        nodes: itertable object of nodes
           Any iterable object that contains nodes
        kwargs: keyword arguments, optional
           Can set features for a node by using key=value.

        Notes
        -----
        When adding multiple nodes with certain features. All of the nodes
        will recieve the same associated key/value pair.

        The runtime is $O(n)$ when adding new nodes, but can degrade to
        $O(n^2)$ when updating features of adding new features to existing
        nodes.

        See add for more details.
        """
        try:
            for node in nodes:
                self.add(node,**kwargs)
        except TypeError:
            return "Nodes object is not iterable"

    def setFeature(self,name,data): 
        """
        Does a one-to-one mapping of data. The data variable must be a
        dictionary where the node name is the key and the data desired to be
        set as the feature called 'name' should be the value. This allows
        a plethora of data to be applied to each node. This mapping can also
        allow for all the data to the nodes to be unique.

        The runtime of this algorithm is $O(n)$ in all cases, since only
        one feature is added.

        Parameters
        ----------
        name: str
           The name of the feature added
        data: dict
           The data is held under a key/value pair in a dictionary. The key must
           be the name of the node and the value is the feature data.

        Notes
        -----
        -> If the data is not in a dictionary format, it will not work.
        """
        try:
            for node,datum in zip(self,data.items()): #loops through node and data
                self.add(node,state = datum[1])
        except AttributeError:
            return "Dictionary must be used"
                

    def getFeature(self,name):
        """
        Returns a dictionary with nodes with feature in question. The key/value
        pair will be as follows: the key will be the name of the node and the
        value will be the data. 

        Parameters
        ----------
        name: str
           the string that represents the name of the node feature.
           By convention the string has all lowercase characters.

        Notes
        -----
        -> The funciton uses a dictionary comprehension
        -> Will not return a dictionary with all nodes if the a node does
           not have that specific feature. 
        """
        return {n: self.graph[n][name] for n in self if name in self.graph[n]}

    def remove(self,node):
        """Removes the nodes from the network.
        Curently it does not remove links that are in the neighbors feature.

        Parameters
        ----------
        node: hashable object
           Any hashable object in the network.

        The runtime is $O(n)$.  
        """
        for x in self:
            neigbhors = self.getNeighbors(x) #gets neighbors for node
            if node in neigbhors: #checks for connection
                (neigbhors).remove(node) #removes any connection
        del self.graph[node] #deletes from graph
        self.nodes.remove(node) #deletes from nodes variable
        return self.graph

    def addEdge(self,node,connection):
        """Adds a link in between two nodes. This is a non-directed link or
        put in another way, a directed link in both directions.

        Parameters
        ----------
        node: hasable object
           Node in the network
        connection: hashable object
           Node in the network

        Will add the node on the other end of the link to the neighbors
        feature.

        Has a runtime of $O(k)$.
        """
        try:
            (self.graph[node]["neighbors"]).add(connection)
            (self.graph[connection]["neighbors"]).add(node)
        except KeyError:
            return "Node not in graph"

    def directedLink(self,node,connection):
        """Adds a link that is directed from node to connection.

        Parameters
        ----------
        node: hasable object
           Node in the network
        connection: hashable object
           Node in the network

        Will only add connection to the neighbors feature of node. This is a
        one way link. 
        """
        try:
            (self.graph[node]["neighbors"]).add(connection)
        except KeyError:
            return "Node not in graph"

    def addMultipleEdges(self,node,connections):
        """
        Adds multiple links to a node, all are non-directed links.

        Parameters
        ----------
        node: hasable object
           Node in the network
        connections: list of hashable objects
           Nodes in the network

        Will add many connections to the network. Will appear in both neighbor
        feature values.

        Has a runtime of $O(n)$.
        """
        try:
            for connection in connections:
                self.addEdge(node,connection) #adds the node between the 
        except TypeError:
            return "Connections object is not iterable"

    def clear(self):
        """
        Clears the network of all links, nodes, and data, the runtime
        is $O(k)$.
        """
        self.graph = dict()
        self.nodes = list()
        self.edge_list = np.zeros([0,0],dtype=int)

    def getNeighbors(self,node):
        """Finds the neighbors between of the node.

        Parameters
        ----------
        node: hashable object
           Any hashable object in the network

        Runtime of $O(k)$.
        """
        return self.graph[node]["neighbors"]

    def edgeList(self):
        """
        Uses the neighbor dictionary to create a numpy array that is the
        adjacency matrix for any network.

        Has a runtime of $O(n^2)$.
        """
        edge_list = np.zeros([len(self),len(self)], dtype = int)
        for node in self:
            for connection in self.graph[node]["neighbors"]:
                edge_list[node,connection] = 1
                edge_list[connection,node] = 1
        return edge_list

    def linksAsTuples(self):
        """
        Returns a list of tuples that can represent each link in a
        network. Where the two nodes in the tuple are the nodes that
        have a connection between them.

        The runtime is $O(n^2)$, however it runs slightly better since it
        uses a map function. 
        """
        tuples = list()
        for x in self:
            edges = list(filter(lambda node: node[0] > x or \
                                node[1] > x,
                                    list(
                                        map(lambda node:(x,node),
                                            self.graph[x]["neighbors"]))))
            tuples = tuples + edges
        return tuples

    def completeGraph(self):
        """
        Takes any network and makes it a complete graph.
        Has a runtime of $O(n^2)$.
        """
        nodes = self.getNodes()
        for item in nodes:
            copy = nodes[:]
            copy.remove(item)
            self.multipleLinkCreator(item,copy)
