"""
Authors: Justin Pusztay, Matt Lubas, Griffin Noe
Filename: cayleygui.py
Project: Research for Irina Mazilu, Ph.D.

Contains the class CayleyGUI, which generates a GUI for Cayley Trees.
"""

import matplotlib
matplotlib.use('TkAgg')
import networkx as nx
import tkinter  as tk
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from cayleytree import CayleyTree
from cayleygraphics import CayleyGraphics
from tkinter import messagebox
import math


class CayleyGUI:
    def __init__(self):
        win_width = 1000
        win_height = 700
        top_height = .1 * win_height
        mid_height = .8 * win_height
        btm_height = .1 * win_height
        
        self.root = tk.Tk()
        self.root.title('Cayley Trees')
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.root.geometry('{}x{}'.format(win_width , win_height))
        

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
        top_frame = tk.Frame(self.root, #bg = top_color,
                          width = win_width, height = top_height)
        mid_frame = tk.Frame(self.root, bg = mid_color,
                          width = win_width, height = mid_height)
        btm_frame = tk.Frame(self.root, bg = btm_color,
                          width = win_width, height = btm_height)

        #Layout Main Containers
        self.root.grid_rowconfigure(0, weight = 1)
        
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
        self.tree_canvas = tk.Canvas(mid_lft, bg = 'black',
                                width = .5 * win_width,
                             height = mid_height)
        gen_label = tk.Label(mid_ctr, bg = midc_color, text='Generations: ')
        lnk_label = tk.Label(mid_ctr, bg = midc_color, text='Connections: ')
        alp_label = tk.Label(mid_ctr, bg = midc_color, text='Alpha: ')
        bet_label = tk.Label(mid_ctr, bg = midc_color, text='Beta: ')
        gam_label = tk.Label(mid_ctr, bg = midc_color, text='Gamma: ')
        self.gen_entry = tk.Entry(mid_ctr)
        self.lnk_entry = tk.Entry(mid_ctr)
        self.alp_entry = tk.Entry(mid_ctr)
        self.bet_entry = tk.Entry(mid_ctr)
        self.gam_entry = tk.Entry(mid_ctr)
        self.gen_entry.insert(0, "3")
        self.lnk_entry.insert(0, "3")
        self.alp_entry.insert(0,".5")
        self.bet_entry.insert(0,".8")
        self.gam_entry.insert(0,".2")
        create_button = tk.Button(mid_ctr, text ='Create',
                                  command = self.create_tree)
        pngtree_button = tk.Button(mid_ctr, text = 'Export PNG',
                                   command = self.export_tree)

        #Layout Middle Widgets
        self.tree_canvas.grid(row = 0, column = 0)
        gen_label.grid(row = 0, column = 0, sticky = "w")
        lnk_label.grid(row = 1, column = 0, sticky = "w")
        alp_label.grid(row = 2, column = 0, sticky = "w")
        bet_label.grid(row = 3, column = 0, sticky = "w")
        gam_label.grid(row = 4, column = 0, sticky = "w")
        self.gen_entry.grid(row = 0, column = 1)
        self.lnk_entry.grid(row = 1, column = 1)
        self.alp_entry.grid(row = 2, column = 1)
        self.bet_entry.grid(row = 3, column = 1)
        self.gam_entry.grid(row = 4, column = 1)
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
        xlsx_button = tk.Button(btm_rht, text = 'Export Excel',
                                command = self.export_xlsx)
        plot_button = tk.Button(btm_rht, text = 'Export PNG',
                                   command = self.export_plot)

        #Layout Bottom Widgets
        step_label.grid(row = 0, column = 0)
        step_slider.grid(row = 1, column = 0)
        xlsx_button.grid(row = 0, column = 0)
        plot_button.grid(row = 0, column = 1)

    def create_tree(self):
        gens  = int(self.gen_entry.get())
        link  = int(self.lnk_entry.get())
        alpha = float(self.alp_entry.get())
        beta  = float(self.bet_entry.get())
        gamma = float(self.gam_entry.get())
        graphic = CayleyGraphics(gens, link)
        plot = graphic.drawCayley()
        photo = self.draw_tree(self.tree_canvas, plot)
        canvas.create_image(0,0, image = photo, anchor = NW)

    def draw_tree(self, canvas, figure, loc = (0,0)):
        """Draws the tree figure onto the tree canvas."""
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

        # Position: convert from top-left anchor to center anchor
        canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo
        
    def export_tree(self):
        return
    
    def export_xlsx(self):
        return
        
    def export_plot(self):
        return

    def update(self):
        self.root.mainloop()

    def quit_app(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.root.destroy()

    def closeEntryWindow(self):
        self.entryWindow.destroy()

def main():
    app = CayleyGUI()
    app.update()

if __name__ == "__main__":
    main()
