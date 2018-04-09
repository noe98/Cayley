#!/usr/bin/env python
"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe, Irina Mazilu
Filename: cayleymain.py
Project: Research for Irina Mazilu, Ph.D.

A main file that runs the Monte Carlo simulation and draws a picture
of the cayley tree.
"""

from montecarlo import MonteCarlo
from cayleygraphics import CayleyGraphics

def main():
    generations = int(input("Number of generations: "))
    links = int(input("Number of links: "))
    print("\n" + "The default values for alpha, beta, gamma are: \n"
          + "Alpha = 0.5 \n"
          + "Beta = 0.8 \n"
          + "Gamma = 0.2 \n")
    custom = input("Do you want to customize alpha, beta, gamma values? [Y/N]: ")
    if(custom.upper()=="Y"):
        alpha = float(input("Value for alpha: "))
        beta = float(input("Value for beta: "))
        gamma = float(input("Value for gamma: "))
        monte = MonteCarlo(generations, links, alpha, beta, gamma)
    else:
        monte = MonteCarlo(generations, links)
    monte.emptyDictionary() #can change to other inital states
    for x in range(len(monte.tree)):
        monte.simulate()
    monte.sendExcel()
    cayley = CayleyGraphics(generations, links)
    cayley.drawCayley()
    
if __name__ == "__main__":
    main()
