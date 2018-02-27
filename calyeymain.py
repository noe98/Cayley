#!/usr/bin/env python
"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe
Filename: cayleymain.py

A main file that runs the Monte Carlo simulation and draws a picture
of the cayley tree.
"""

#Added comment

from cayleytree import CayleyTree
from montecarlo import MonteCarlo
from cayleygraphics import CayleyGraphics

def main():
    generations = int(input("Number of generations: "))
    links = int(input("Number of links: "))
    alpha = float(input("Value for alpha: "))
    beta = float(input("Value for beta: "))
    gamma = float(input("Value for gamma: "))
    a = MonteCarlo(generations, links)
    a.setAlpha(alpha)
    a.setBeta(beta)
    a.setGamma(gamma)
    a.emptyDictionary() #can change to other inital states
    a.simulate()
    a.sendExcel()

    #b = CayleyGraphics(generations, links)
    #b.drawGraph()
    
if __name__ == "__main__":
    main()
