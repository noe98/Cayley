"""
Example code for how to set up a simulation that needs temperature data.

This module run a Cayley Tree.
"""

import Cayley as cy

#Creating network and monte carlo objects
network = cy.CayleyTree(3,3)
monte = cy.MonteCarlo(network)

#Set temperature of each generation
"""
This gives each generation a temperature its own temperature.
The best way to get all of the nodes in a generation of CayleyTree is
nodeFinder(gen). It has a runtime of $O(k)$, where k is a constant. The
runtime is constant.
"""

monte.temperature(network.nodesPerGen(0),10)
monte.temperature(network.nodesPerGen(1),20)
monte.temperature(network.nodesPerGen(2),40)
monte.temperature(network.nodesPerGen(3),80)

#Showing the temperature feature dictionary from network
print("Temperature Dictionary")
print(network.getNodeFeature('temperature'))

#starts all nodes empty
monte.emptyDictionary()

#Running simulation using temperature method
for x in range(len(network)):
    monte.simulateTemp()
