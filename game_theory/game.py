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

from Cayley import Graph
import Cayley.game_theory as cgt
import csv

issue_rating = 0.25
a = 1
b = 10
c = 100
d = 1000
k = 500
timesteps = 2
name_of_excel_sheet = '%da_%db_%dc_%dd' %(a,b,c,d)


def main():

    # Issue occurs since the reps share the same last name
    # Entries in a python dictionary must be unique
    
    import random
    with open("houseData.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0
        a = dict()
        for row in readCSV:
            print(count);print(row[8])
            if row[8] in a:
                print(row[8]," is a repeat")
            a[row[8]] = random.randint(0,1)
            count+=1
        print(len(a))
##    strategy_data_dump = list()
##    real_data_dump = list()
##    imagined_data_dump = list()
##    g = Graph()
##    cgt.make_senate(g)
####    g.completeGraph()
##    for node in g: #adds one random agent
##        cgt.random_agent(g,node)
##    cgt.random_strat_start(g)
##    strategy_data_dump.append(g.getNodeFeature('strategy'))
##    for step in range(timesteps):
##        cgt.timestep(g,issue_rating,a,b,c,d,k)
##        strategy_data_dump.append(g.getNodeFeature('strategy'))
##        real_data_dump.append(g.getNodeFeature('real_reward'))
##        imagined_data_dump.append(g.getNodeFeature('imagined_reward'))
##    #print(real_data_dump)
##    cgt.export_data(name_of_excel_sheet,g,strategy_data_dump,real_data_dump,
##                                    imagined_data_dump)
##    
##        #cgt.data_export(name_of_excel_sheet,g)

if __name__ == '__main__':
    main()
