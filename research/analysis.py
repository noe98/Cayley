"""
@author: Justin Pusztay

Here we craft functions for data anaylsis from monte carlo simulations
run on Cayley trees. 
"""

__all__ = ['density','final_state','density_generations','correlation']

def density(network,monte):
    """Stores the density of the each timestep per trial"""
    density = dict()
    for x in range(monte.getTimesteps()):
        d = (monte.getOnes(x))/(len(network))
        density[x] = d
    return density
    
def final_state(monte):
    """Stores the final state for each node in a timestep of a trial"""
    return monte.allData()[-1]
        
def density_generations(network,monte):
    """Stores the density of a each generation in a list for each timestep."""
    # [Generation][Timestep] = density of generation at timestep
    density_generations = dict()
    for x in range(network.generations+1):
        denstiy_timestep = dict()
        for y in range(monte.getTimesteps()):
            denstiy_timestep[y] =  monte.generationalDensity(x,monte.simData(y))
        density_generations[x] = denstiy_timestep
    return density_generations
            
def correlation(network,monte,node,other_node):
    """Finds the correlation between any two nodes for a trial."""
    sum_of_products = 0
    sum_node = 0
    sum_other = 0

    for timestep in monte.allData():
        if timestep[node] == 0:
            sum_of_products += (2*timestep[node]-1)*(2*timestep[other_node]-1)
            sum_node += (2*timestep[node]-1)
            sum_other += (2*timestep[other_node]-1)

    print("products: ",sum_of_products)
    print("node sum: ",sum_node)
    print("other sum: ",sum_other) 
    
    a = monte.getTimesteps()
    print("timesteps ",a)
    correlation = (sum_of_products/a) - ((sum_node/a)*(sum_other/a))
    return correlation
        
