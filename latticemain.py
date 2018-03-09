#!/usr/bin/env python
"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe
Filename: latticemain.py
Project: Research for Irina Mazilu, Ph.D.

A main file that runs the Monte Carlo simulation and draws a picture
of the Lattice tree.
"""

from montecarlo import MonteCarlo
from latticegraphics import LatticeGraphics

def main():
    
    """
    generations = int(input("Number of generations: "))
    links = int(input("Number of links: "))
    custom = input("Custom A, B, G Values? [Y/N]: ")
    if(custom.upper()=="Y"):
        alpha = float(input("Value for alpha: "))
        beta = float(input("Value for beta: "))
        gamma = float(input("Value for gamma: "))
        monte = MonteCarlo(generations, links, alpha, beta, gamma)
    else:
        monte = MonteCarlo(generations, links)
    monte.emptyDictionary() #can change to other inital states
    monte.simulate()
    monte.sendExcel()
    """

    a = LatticeGraphics()
    a.drawLattice(a.GraphList)
    
if __name__ == "__main__":
    main()
