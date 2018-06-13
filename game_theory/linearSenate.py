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
print(senate_network)

##def senate(network,csv_file = 'senatedata.csv'):
##    with open(csv_file) as csvfile:
##        readCSV = csv.reader(csvfile, delimiter=',')
##        for row in readCSV:
##            if row[8] != 'name':
##                print(row[8])
##                network.add(row[8],ideology = row[3],state = row[6])

##senate(senate_network)
