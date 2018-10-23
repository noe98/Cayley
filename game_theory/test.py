import Cayley as cy
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

strategy_data_dump = list()
real_data_dump = list()
imagined_data_dump = list()

g = cy.Graph()

cgt.make_senate(g,'houseData.csv')


for rep in g:
    cgt.random_agent(g,rep)
cgt.random_strat_start(g)
strategy_data_dump.append(g.getNodeFeature('strategy'))
for step in range(timesteps):
    cgt.timestep(g,issue_rating,a,b,c,d,k)
    strategy_data_dump.append(g.getNodeFeature('strategy'))
    real_data_dump.append(g.getNodeFeature('real_reward'))
    imagined_data_dump.append(g.getNodeFeature('imagined_reward'))
cgt.export_data(name_of_excel_sheet,g,strategy_data_dump,real_data_dump,
                imagined_data_dump)
