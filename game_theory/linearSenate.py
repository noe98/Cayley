import Cayley as cy
import csv

def senators(csv_file = 'senatedata.csv'):
    senators = list()
    with open(csv_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[8] != 'name':
                senators.append(row[8])
    return senators

senate = senators()

senate_network = cy.Lattice(100,1,names = senate)

center = 0.5
##senate_network.center = some function for median of scores
##senate_network.issue = idealogical score of issue

def ideals(network,csv_file = 'senatedata.csv'):
    with open(csv_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[8] != 'name':
                network.add(row[8],ideology = float(row[3]),rank = row[0])

ideals(senate_network)

def beta_phi(network):
    for x in network:
        network.add(x,beta=1/(abs(network.graph[x]['ideology']-center)),\
                    phi = 1/(abs(network.graph[x]['ideology']-center)))
    

beta_phi(senate_network)
