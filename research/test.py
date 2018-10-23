"""
@author: Justin Pusztay
"""

# In this file we will only worry about 'NN' simulations
# In this file we only start from empty with the states.

"""
Average is multiplying states of two nodes and dividing by number of timesteps
"""

import Cayley as cy
import Cayley.research as cr
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
        
def main():
    # Set up for simulation
    generations = 3
    links = 3
    alpha = 0.5
    beta = 0.2
    gamma = 0.2
    mu = 0.2
    r1 = 0.5
    r2 = 0.5
    trials = 50
    k = 12
    J = 10
    timesteps = 10
    b = cy.CayleyTree(generations,links)
    monte = cy.MonteCarlo(b, alpha, beta, gamma, mu, r1, r2)
    monte.startEmpty()

    # Runs one trial
    # # # # # # # # # # # # # 
    for x in range(timesteps):
        monte.simulateNN()
    # # # # # # # # # # # # #

    # Generates statistics about trial
    a = cr.density(b,monte)
    cr.final_state(monte)
    c = cr.density_generations(b,monte)
    
    # Densities per timestep plot
    plt.plot(a.values())
    plt.ylabel('density')
    plt.xlabel('timestep')
    plt.show()
    
    # Final state graphics
    G = nx.Graph()
    color_map = list()
    for node in b:
        if monte.previousState(node) == 0:
            color_map.append('green')
        else:
            color_map.append('red')
    G.add_nodes_from(b)
    G.add_edges_from(b.linksAsTuples())
    nx.draw(G,node_color = color_map,with_labels = True)
    plt.show()

    generation = 0
    for x in c.values():
        plt.plot(x.values(),label = "Generation "+str(generation))
        generation += 1
    plt.ylabel("Generational Density")
    plt.xlabel("timestep")
    plt.legend()
    plt.show()
    
if __name__ == "__main__":
    main()
