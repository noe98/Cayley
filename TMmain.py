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

    monte.randomSpins()
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
