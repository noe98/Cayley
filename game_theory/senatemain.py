import Cayley as cy
import Cayley.game_theory as cg
from Cayley.change_me import timesteps
import csv

def main():
    print("Enter 'Linear' or 'Complete' for model type.")
    model = input('Model: ').lower()
    senate_list = cg.senators('senatedata.csv')

    if model == 'linear':
        network = cy.Lattice(100,1,names = senate_list)
    
    issue = float(input("What is the issue rating? "))
    polarity = abs(issue-0.5)
    cg.ideals(network)
    cg.beta_phi(network)
    senate = cy.MonteCarlo(network, 1/polarity)
    senate.gamma = senate.alpha
    senate.center = 0.5 ### CHANGE ###
    senate.randomDictionary() ### CHANGE###

    for i in range(timesteps):
        senate.simulateVote()

    senate.sendExcel()

if __name__ == '__main__':
    main()
