import xlwt
import math
import random

node_dict = dict()
for x in range(20):
    node_dict[x] = random.randint(0,1)
    
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
rows = list()
cols = list()
sheet1.write(0,0,"Time Step")
for key in node_dict:
    sheet1.write(key+1, 0,"Node " + str(key))
    sheet1.write(0,key+1, key)
for key in node_dict:
    sheet1.write(key+1,1,node_dict[key])
book.save("trial.xls")

##import csv
##import math
##import random
##node_dict = dict()
##for x in range(20):
##    itemName = 'node ' + str(x)
##    node_dict[itemName] = x
##edges_d = list(range(pow(len(node_dict),2)))
##
##with open('test.csv', 'w') as f:
##    w = csv.writer(f, delimiter=',')
##with open('test.csv', 'w') as f:
##    w = csv.DictWriter(f, node_dict)
##    w.writeheader()
##    w.writerow(node_dict)

##print(node_dict)
