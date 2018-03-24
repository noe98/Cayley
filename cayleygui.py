"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe
Filename: cayleygui.py
Project: Research for Irina Mazilu, Ph.D.

Contains the class CayleyGUI, which generates a GUI for Cayley Trees.
"""

import networkx as nx
import matplotlib.pyplot as plt
from cayleytree import CayleyTree
import tkinter as tk

class CayleyGUI:
    def __init__(self,parent):
        win_width = 1000
        win_height = 700
        top_height = .1 * win_height
        mid_height = .8 * win_height
        btm_height = .1 * win_height
        
        self.parent = parent
        parent.title('Cayley Trees')
        parent.geometry('{}x{}'.format(win_width,win_height))

        top_color = 'blue'
        mid_color = 'pink'
        btm_color = 'grey'

        midl_color = 'brown1'
        midc_color = 'cadetblue1'
        midr_color = 'chartreuse1'
        
        btml_color = 'brown3'
        btmc_color = 'cadetblue3'
        btmr_color = 'chartreuse3'

        #Create Main Containers
        top_frame = tk.Frame(parent, #bg = top_color,
                          width = win_width, height = top_height)
        mid_frame = tk.Frame(parent, bg = mid_color,
                          width = win_width, height = mid_height)
        btm_frame = tk.Frame(parent, bg = btm_color,
                          width = win_width, height = btm_height)

        #Layout Main Containers
        parent.grid_rowconfigure(0, weight = 1)
        
        top_frame.grid(row=0, sticky = 'w')
        mid_frame.grid(row=1)
        btm_frame.grid(row=2)

        #Create Top Frame Widgets
        st_label = tk.Label(top_frame,
                                  text = 'Select Starting State: ')
        cen_tick = tk.Checkbutton(top_frame,
                                  text = 'Center')
        ran_tick = tk.Checkbutton(top_frame, 
                                  text = 'Random')
        flt_tick = tk.Checkbutton(top_frame, 
                                  text = 'Flat')

        #Layout Top Widgets
        st_label.grid(row = 0, column = 0)
        cen_tick.grid(row = 0, column = 1)
        ran_tick.grid(row = 0, column = 2)
        flt_tick.grid(row = 0, column = 3)

        #Create Middle Frames
        mid_lft = tk.Frame(mid_frame, bg = midl_color, width = .5 * win_width,
                            height = mid_height)
        mid_ctr = tk.Frame(mid_frame, bg = midc_color, width = .15 * win_width,
                            height = mid_height)
        mid_rht = tk.Frame(mid_frame, bg = midr_color, width = .35 * win_width,
                            height = mid_height)

        #Layout Middle Frames
        mid_lft.grid(row = 0, column = 0)
        mid_ctr.grid(row = 0, column = 1)
        mid_rht.grid(row = 0, column = 2)

        #Create Middle Widgets
        tree_canvas = tk.Canvas(mid_lft, bg = 'black',
                                width = .5 * win_width,
                             height = mid_height)
        gen_label = tk.Label(mid_ctr, bg = midc_color, text='Generations: ')
        conn_label = tk.Label(mid_ctr, bg = midc_color, text='Connections: ')
        alpha_label = tk.Label(mid_ctr, bg = midc_color, text='Alpha: ')
        beta_label = tk.Label(mid_ctr, bg = midc_color, text='Beta: ')
        gamma_label = tk.Label(mid_ctr, bg = midc_color, text='Gamma: ')
        gen_entry = tk.Entry(mid_ctr)
        conn_entry = tk.Entry(mid_ctr)
        alpha_entry = tk.Entry(mid_ctr)
        beta_entry = tk.Entry(mid_ctr)
        gamma_entry = tk.Entry(mid_ctr)
        create_button = tk.Button(mid_ctr, text ='Create')
        pngtree_button = tk.Button(mid_ctr, text = 'Export PNG')

        #Layout Middle Widgets
        tree_canvas.grid(row = 0, column = 0)
        gen_label.grid(row = 0, column = 0, sticky = "w")
        conn_label.grid(row = 1, column = 0, sticky = "w")
        alpha_label.grid(row = 2, column = 0, sticky = "w")
        beta_label.grid(row = 3, column = 0, sticky = "w")
        gamma_label.grid(row = 4, column = 0, sticky = "w")
        gen_entry.grid(row = 0, column = 1)
        conn_entry.grid(row = 1, column = 1)
        alpha_entry.grid(row = 2, column = 1)
        beta_entry.grid(row = 3, column = 1)
        gamma_entry.grid(row = 4, column = 1)
        create_button.grid(row = 5, column = 0, sticky = 'w')
        pngtree_button.grid(row = 6, column = 0, sticky = 'w')

        #Create Bottom Frames
        btm_lft = tk.Frame(btm_frame, bg = btml_color, width = .50 * win_width,
                            height = btm_height)
        btm_ctr = tk.Frame(btm_frame, bg = btmc_color, width = .15 * win_width,
                            height = btm_height)
        btm_rht = tk.Frame(btm_frame, bg = btmr_color, width = .35 * win_width,
                            height = btm_height)

        #Layout Bottom Frames
        btm_frame.grid_columnconfigure(1, weight = 1)
        
        btm_lft.grid(row = 0, column = 0)
        btm_ctr.grid(row = 0, column = 1)
        btm_rht.grid(row = 0, column = 2)

        #Create Bottom Widgets
        step_label = tk.Label(btm_lft, bg = btml_color, text = 'Time Steps')
        step_slider = tk.Scale(btm_lft, from_ = 0, to = 100,
                            orient = 'horizontal')
        xlsx_button = tk.Button(btm_rht, text = 'Export Excel')
        pngplot_button = tk.Button(btm_rht, text = 'Export PNG')

        #Layout Bottom Widgets
        step_label.grid(row = 0, column = 0)
        step_slider.grid(row = 1, column = 0)
        xlsx_button.grid(row = 0, column = 0)
        pngplot_button.grid(row = 0, column = 1)

        
def main():
    root = tk.Tk()
    app = CayleyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
