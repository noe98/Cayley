"""
Sets arbitrary values of variables to be referenced by volume.py.
"""

timesteps = 50
node_list = [[0,1],[0,4]]
#    Format [[1 node in 1 pair, 2 node in 1 pair],[1 node in 2 pair, 2 node in 2 pair],...]
initial_state = "empty"
#    Can be either "empty", "random", or "zero"

total_nodes = [[1,None,None,None,None], #total_nodes[gens][links]
               [None,2,3,4,5,6],
               [None,None,5,10,17,26],
               [None,None,7,22,53,106],
               [None,None,9,46,161,426],
               [None,None,11,94,485,1706]]

alpha_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
beta_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
gamma_list = [0, 0.05, 0.1, 0.15, 0.2]
mu_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
r1_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
r2_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

temp_d = {0: 0.3,
          1: 0.2,
          2: 0.3,
          3: 0.2,
          4: 0.3,
          5: 0.2,
          6: 0.3
          }

senate_corr = [] #[['Franken','Sanders'],['Sanders','Merkley']]
