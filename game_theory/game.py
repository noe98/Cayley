"""
Runs a game simulation for the senate.

Warnings
--------
-> Currently the timestep function just picks a random agent when
   iterating through the network to play with.
-> Initial strategies are not put into excel.
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
timesteps = 50
name_of_excel_sheet = 'test'

def main():
    g = cy.Graph()
    cgt.senate(g)
    cgt.random_strat_start(g)
    for step in range(timesteps):
        cgt.timestep(g,issue_rating,a,b,c,d,k)
        cgt.data_export(name_of_excel_sheet,g)

if __name__ == '__main__':
    main()
