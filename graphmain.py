#!/usr/bin/env python
"""
Authors: Justin K. Pusztay
Filename: graphmain.py
Project: Research for Irina Mazilu, Ph.D.

Below is an example of a custom graph being created and a MonteCarlo simulation
being run on the graph.
"""

from graph import Graph
from montecarlo import MonteCarlo

def main():
    a = Graph()
    a.add("Justin")
    a.add("Maria")
    a.add("Joe")
    a.add("John")
    a.add("Cole")
    a.linkCreator("Justin","Maria")
    a.linkCreator("Justin","Joe")
    a.linkCreator("Joe","Cole")
    a.linkCreator("Maria","John")
    print(a.link_d)
    monte = MonteCarlo(a)
    monte.emptyDictionary()
    print(monte.emptyDictionary())
    for x in range(len(monte.network)):
        monte.simulate()
    monte.sendExcel()

if __name__ == "__main__":
    main()
