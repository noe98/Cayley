"""
"""

import Cayley as cy
import Cayley.graphics as cg

def main():
    generations = int(input("Number of generations: "))
    links = int(input("Number of links: "))
    network = cy.CayleyTree(generations,links)

    print("\n" + "The default values for k and J are 1.")
    custom = input("Do you want to customize these values? [Y/N]: ")
    if(custom.upper()=='Y'):
        k = float(input("Value for k: "))
        J = float(input("Value for J: "))
    else:
        k = J = 1
    monte = cy.MonteCarlo(network) # Edit later

    print("\n" + "Enter Excel file name \n"
          + "Example: monteCarloData")
    filename = str(input("Filename: "))
    full_filename = filename + ".xlsx"

    print("Press 1 for starting all nodes empty. \n" +
          "Press 2 for starting random percentage of nodes filled. \n" +
          "Press 3 for only having the 0 node filled.")
    num_select = int(input("Starting state: "))
    if num_select == 1:
        monte.emptyDictionary() #can change to other inital states
    elif num_select == 2:
        monte.randomDictionary()
    else:
        monte.zeroDictionary()
    for i in range (generations+1):
        temp = float(input("Temperature of generation %s: " %(i)))
        network.addMultipleNodes(network.nodesPerGen(i),temperature=temp)
    for x in range(len(network)):
        monte.simulateTemp(k,J)

    monte.sendExcel(full_filename)
    cayley = cg.CayleyGraphics(generations, links)
    cayley.drawCayley()

if __name__ == "__main__":
    main()


## Needs parameters, different temp settings, etc.
## de-parameterize simulate() methods?
