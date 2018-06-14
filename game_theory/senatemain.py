import Cayley as cy
import Cayley.game_theory as cg
from Cayley.change_me import timesteps
import csv

def main():
    print("Enter 'Linear', 'Limited', or 'Complete' for model type.")
    model = input('Model: ').lower()
    senate_list = senators('senatedata.csv')
    network = cy.Lattice(100,1,names = senate_list)
    network.center = 0.5 ### ALTER ###  
    ideals(network)
    const = float(input("Input proportionality constant for beta and phi: "))
    beta_phi(network, const)

    if model == 'complete':
        network.completeGraph()
    if model == 'limited':
        radius = float(input("Radius of connection: "))
        network.limitedGraph(radius)
    
    issue = float(input("What is the issue rating? "))
    print("\n" + "Enter Excel file name \n"
          + "Example: monteCarloData")
    filename = str(input("Filename: "))
    full_filename = filename + ".xlsx"
    polarity = issue-0.5
    const = float(input("Input proportionality constant for alpha and gamme: "))
    senate = cy.MonteCarlo(network, 1/(const*abs(polarity)))
    senate.median = 0.5 ## CHANGE ###
    senate.gamma = senate.alpha
    senate.senateDictionary(issue) ### CHANGE###

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

def beta_phi(network, constant):
    for x in network:
        partisan = network.graph[x]['ideology']-network.center
        network.add(x,beta=1/(constant*abs(partisan)),\
                    phi = 1/(constant*abs(partisan)))

if __name__ == '__main__':
    main()


### SENATE CENTER ###
