"""
Runs a game simulation for the senate.

Warnings
--------
-> Currently the timestep function just picks a random agent when
   iterating through the network to play with.
-> Initial strategies are put into excel for the 0 timestep!
-> Strategy sheet will have an extra timestep since orignial strategies are listed.
-> Every senator only plays the game with one other person in a timestep.
"""

import Cayley as cy
import Cayley.game_theory as cgt

issue_rating = 0.25
a = 1
b = 10
c = 100
d = 1000
k = 500
timesteps = 2
name_of_excel_sheet = 'test'

def main():
    strategy_data_dump = list()
    real_data_dump = list()
    imagined_data_dump = list()
    g = cy.Graph()
    cgt.senate(g)
##    g.completeGraph()
    for node in g: #adds one random agent
        cgt.random_agent(g,node)
    cgt.random_strat_start(g)
    strategy_data_dump.append(g.getNodeFeature('strategy'))
    for step in range(timesteps):
        cgt.timestep(g,issue_rating,a,b,c,d,k)
        strategy_data_dump.append(g.getNodeFeature('strategy'))
        real_data_dump.append(g.getNodeFeature('real_reward'))
        imagined_data_dump.append(g.getNodeFeature('imagined_reward'))
    #print(real_data_dump)
    cgt.export_data(name_of_excel_sheet,g,strategy_data_dump,real_data_dump,
                                    imagined_data_dump)
    
        #cgt.data_export(name_of_excel_sheet,g)

if __name__ == '__main__':
    main()
