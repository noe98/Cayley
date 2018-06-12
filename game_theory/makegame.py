import csv
import Cayley as cy
import numpy as np

network = cy.Graph()

name_of_data_from_csv = ['rank_from_low', 'rank_from_high',
                         'percentile', 'ideology', 'id',
                         'bioguide_id', 'state', 'district', 'name']

def senate():
    """Creates an empty copy of a senate with senator name,senator
    idealogy, and state.The name is the name of the node."""
    with open('senatedata.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[8] != 'name':
                network.add(row[8],ideology = row[3],state = row[6])

def payoff_matrix1(a,b,c,d,agent1,agent2):
    """Payoff Matrix for issue value less than 0.5 and
    agent with score less than 0.5"""
    a1 = float(network.getNodeFeature('ideology')[agent1])
    a2 = float(network.getNodeFeature('ideology')[agent2])
    matrix1 = np.matrix([[a*abs(a1-a2),b*abs(a1-a2)],
                         [c*abs(a1-a2),d*abs(a1-a2)]],dtype = float)
    return matrix1

def payoff_matrix2(a,b,c,d,agent1,agent2):
    """Payoff Matrix for issue value less than 0.5 and
    agent with score more than 0.5"""
    a1 = float(network.getNodeFeature('ideology')[agent1])
    a2 = float(network.getNodeFeature('ideology')[agent2])
    matrix2 = np.matrix([[d*abs(a1-a2),c*abs(a1-a2)],
                         [b*abs(a1-a2),a*abs(a1-a2)]],dtype = float)
    return matrix2

def payoff_matrix3(a,b,c,d,agent1,agent2):
    """Payoff Matrix issue value greater than 0.5 and
    agent with score less than 0.5"""
    a1 = float(network.getNodeFeature('ideology')[agent1])
    a2 = float(network.getNodeFeature('ideology')[agent2])
    matrix3 = np.matrix([[d*abs(a1-a2),c*abs(a1-a2)],
                         [b*abs(a1-a2),a*abs(a1-a2)]],dtype = float)
    return matrix2

def payoff_matrix4(a,b,c,d,agent1,agent2):
    """Payoff Matrix issue value greater than 0.5 and
    agent with score less than 0.5"""
    a1 = float(network.getNodeFeature('ideology')[agent1])
    a2 = float(network.getNodeFeature('ideology')[agent2])
    matrix4 = np.matrix([[a*abs(a1-a2),b*abs(a1-a2)],
                         [c*abs(a1-a2),d*abs(a1-a2)]],dtype = float)
    return matrix4

def getRating(agent):
    return float(network.getNodeFeature('ideology')[agent])


senate()
#print(payoff_matrix1(1,10,100,1000,'Brown','Cruz'))


