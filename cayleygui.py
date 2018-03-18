"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe
Filename: cayleygui.py
Project: Research for Irina Mazilu, Ph.D.

Contains the class CayleyGraphics, which generates a GUI for the
Cayley Tree. 

Code Adapted from: https://www.udacity.com/wiki/creating-network-graphs-with-python
"""

import networkx as nx
import matplotlib.pyplot as plt
from cayleytree import CayleyTree
from tkinter import *


root = Tk()
root.title("Cayley Trees")
root.geometry('{}x{}'.format(460,350))
frame = Frame(root, bg='white',width=460,height=350)
root.mainloop()

        
