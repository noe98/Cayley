import Cayley as cy
import Cayley.game_theory as cg
from Cayley.change_me import timesteps
import csv

def main():
    print("Enter 'Linear' or 'Complete' for model type.")
    model = input('Model: ').lower()
    senate_list = senators('senatedata.csv')
    network = cy.Lattice(100,1,names = senate_list)

    if model == 'complete':
        network.completeGraph()
    
    issue = float(input("What is the issue rating? "))
    print("\n" + "Enter Excel file name \n"
          + "Example: monteCarloData")
    filename = str(input("Filename: "))
    full_filename = filename + ".xlsx"
    polarity = abs(issue-0.5)
    network.center = 0.5 ### CHANGE ###
    ideals(network)
    beta_phi(network)
    senate = cy.MonteCarlo(network, 1/polarity)
    senate.gamma = senate.alpha
    senate.randomDictionary() ### CHANGE###

    for i in range(timesteps):
        senate.simulateVote()

    senate.sendExcel(full_filename)

def senators(csv_file = 'senatedata.csv'):
    senators = list()
    with open(csv_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[8] != 'name':
                senators.append(row[8])
    return senators

def ideals(network,csv_file = 'senatedata.csv'):
    with open(csv_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[8] != 'name':
                network.add(row[8],ideology = float(row[3]),rank = row[0])

def beta_phi(network):
    for x in network:
        network.add(x,beta=1/(abs(network.graph[x]['ideology']-network.center)),\
                    phi = 1/(abs(network.graph[x]['ideology']-network.center)))

if __name__ == '__main__':
    main()
