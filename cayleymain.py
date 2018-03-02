#!/usr/bin/env python
"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe
Filename: cayleymain.py

A main file that runs the Monte Carlo simulation and draws a picture
of the cayley tree.
"""

from montecarlo import MonteCarlo
from cayleygraphics import CayleyGraphics

def main():
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

    cayley = CayleyGraphics(generations, links)
    cayley.drawGraph()
    
if __name__ == "__main__":
    main()