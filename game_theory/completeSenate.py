import Cayley as cy
import csv

def senators(csv_file = 'senatedata.csv'):
    """Creates a list of the senators names."""
    senators = list()
    with open(csv_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[8] != 'name':
                senators.append(row[8])
    return senators

senate = senators()

senate_network = cy.Lattice(100,1,names = senate)
senate_network.completeGraph()

