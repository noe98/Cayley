#!/usr/bin/env python
"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe
Filename: latticemain.py
Project: Research for Irina Mazilu, Ph.D.

A main file that runs the Monte Carlo simulation and draws a picture
of the Lattice tree.
"""

import Cayley as cy
import Cayley.graphics as cg

def main():
    x_dir = int(input("What is length? "))
    y_dir = int(input("What is width? "))
    z_dir = int(input("What is height? "))
    print("\n" + "The default values for alpha, beta, gamma are: \n"
          + "Alpha = 0.5 \n"
          + "Beta = 0.8 \n"
          + "Gamma = 0.2 \n")
    custom = input("Do you want to customize alpha, beta, gamma values? [Y/N]: ")
    network = cy.Lattice(x_dir,y_dir,z_dir)
    if(custom.upper()=="Y"):
        alpha = float(input("Value for alpha: "))
        beta = float(input("Value for beta: "))
        gamma = float(input("Value for gamma: "))
        monte = cy.MonteCarlo(network, alpha, beta, gamma)
    else:
        monte = cy.MonteCarlo(network)
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
    for x in range(len(network)):
        monte.simulateNN()
    monte.sendExcel(full_filename)
    a = cg.LatticeGraphics(x_dir,y_dir,z_dir)
    a.drawLattice()
    
if __name__ == "__main__":
    main()
