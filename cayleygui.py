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

top_color = 'cyan'
mid_color = 'pink'
btm_color = 'white'
ctrl_color = 'yellow'
ctrm_color = 'magenta'
ctrr_color = 'green'

root = Tk()
root.title('Cayley Trees')
root.geometry('{}x{}'.format(800, 350))

# create all of the main containers
top_frame = Frame(root, bg= top_color, width=450, height=50, pady=3)
center = Frame(root, bg= mid_color, width=450, height=250, padx=3, pady=3)
btm_frame = Frame(root, bg= btm_color, width=450, height=50, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")

# create the widgets for the top frame
starting_label = Label(top_frame, bg = top_color, text='Select Starting State:')
center_tick = Checkbutton(top_frame, bg = top_color, text = 'Center')
random_tick = Checkbutton(top_frame, bg = top_color, text = 'Random')
flat_tick = Checkbutton(top_frame, bg = top_color, text = 'Flat')

# layout the widgets in the top frame
starting_label.grid(row=0, columnspan=2)
center_tick.grid(row=0,column=2)
random_tick.grid(row=0,column=3)
flat_tick.grid(row=0,column=4)

# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = Frame(center, bg=ctrl_color, width=350, height=250)
tree_canvas = Canvas(ctr_left,width=350,height=250)
ctr_mid = Frame(center, bg=ctrm_color, width=150, height=190, padx=3, pady=3)
gen_label = Label(ctr_mid, bg = ctrm_color, text='Generations: ')
conn_label = Label(ctr_mid, bg = ctrm_color, text='Connections: ')
alpha_label = Label(ctr_mid, bg = ctrm_color, text='Alpha: ')
beta_label = Label(ctr_mid, bg = ctrm_color, text='Beta: ')
gamma_label = Label(ctr_mid, bg = ctrm_color, text='Gamma: ')
gen_entry = Entry(ctr_mid)
conn_entry = Entry(ctr_mid)
alpha_entry = Entry(ctr_mid)
beta_entry = Entry(ctr_mid)
gamma_entry = Entry(ctr_mid)
create_button = Button(ctr_mid,text='Create')
pngtree_button = Button(ctr_mid,text ='Export PNG')


ctr_right = Frame(center, bg=ctrr_color , width=300, height=190, padx=3, pady=3)
plot_canvas = Canvas(ctr_right,width=300,height=90)
excel_canvas = Canvas(ctr_right,width=300,height=90)

ctr_left.grid(row=0, column=0, sticky="ns")
tree_canvas.grid(row=0,column=0)
ctr_mid.grid(row=0, column=1, sticky="nsew")
gen_label.grid(row=0,column=0,sticky="w")
conn_label.grid(row=1,column=0,sticky="w")
alpha_label.grid(row=2,column=0,sticky="w")
beta_label.grid(row=3,column=0,sticky="w")
gamma_label.grid(row=4,column=0,sticky="w")
gen_entry.grid(row=0, column=1)
conn_entry.grid(row=1, column=1)
alpha_entry.grid(row=2, column=1)
beta_entry.grid(row=3, column=1)
gamma_entry.grid(row=4, column=1)
create_button.grid(row=5,column=0,sticky='nsew')
pngtree_button.grid(row=6,column=0,sticky='nsew')
ctr_right.grid(row=0, column=2, sticky="ns")
plot_canvas.grid(row=0,column=0, sticky='n')
excel_canvas.grid(row=1,column=0, sticky='s')

# create the bottom widgets
step_label = Label(btm_frame, bg = btm_color, text = 'Time Steps')
step_slider = Scale(btm_frame, from_=0, to=100,
                    orient = HORIZONTAL)
xlsx_button = Button(btm_frame, text = 'Export Excel')
pngplot_button = Button(btm_frame,text='Export PNG')

step_label.grid(row=0,column=0)
step_slider.grid(row=1,column=0)
xlsx_button.grid(row=0,column=1,sticky='e')
pngplot_button.grid(row=0,column=2,sticky='e')


root.mainloop()
        
