import PageTemplate
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as backend_tkagg

import wall_calculations


class WallPage(PageTemplate.Page):
    def __init__(self, *args, **kwargs):
        PageTemplate.Page.__init__(self, *args, **kwargs)

        self.fig_hole = mpl.figure.Figure(dpi=125)
        self.plot = self.fig_hole.add_subplot(111)

        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig_hole, self)
        self.canvas.get_tk_widget().grid(row=3, column=1, columnspan=6)

        self.toolbar = backend_tkagg.NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.grid(row=4, column=1, columnspan=6)

        self.omega = tk.DoubleVar()
        self.omega.set(1)
        self.omega_label = ttk.Label(self, text="omega * a")
        self.omega_entry = ttk.Entry(self, width=10, textvariable=self.omega)
        self.omega_label.grid(row=1, column=1)
        self.omega_entry.grid(row=2, column=1)

        self.mass = tk.DoubleVar()
        self.mass.set(9e-31)
        self.mass_label = ttk.Label(self, text="Mass")
        self.mass_entry = ttk.Entry(self, width=10, textvariable=self.mass)
        self.mass_label.grid(row=1, column=2)
        self.mass_entry.grid(row=2, column=2)

        self.a = tk.DoubleVar()
        self.a.set(1e-9)
        self.a_label = ttk.Label(self, text="a")
        self.a_entry = ttk.Entry(self, width=5, textvariable=self.a)
        self.a_label.grid(row=1, column=3)
        self.a_entry.grid(row=2, column=3)

        self.n = tk.IntVar()
        self.n.set(2)
        self.n_label = ttk.Label(self, text="Function number")
        self.n_entry = ttk.Entry(self, width=5, textvariable=self.n)
        self.n_label.grid(row=1, column=4)
        self.n_entry.grid(row=2, column=4)

        self.simulate_label = ttk.Label(self, text="Simulate")
        self.simulate_button = ttk.Button(self, text="Run", command=self.simulate)
        self.simulate_label.grid(row=1, column=5)
        self.simulate_button.grid(row=2, column=5)

    def simulate(self):
        self.fig_hole = mpl.figure.Figure(dpi=125)
        self.plot = self.fig_hole.add_subplot(111)

        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig_hole, self)
        self.canvas.get_tk_widget().grid(row=3, column=1, columnspan=6)

        self.toolbar = backend_tkagg.NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.grid(row=4, column=1, columnspan=6)

        self.xs, self.uss = wall_calculations.calculate(self.mass.get(), self.a.get(), self.omega.get(), self.n.get())
        max_u = 0
        for us in self.uss:
            self.plot.plot(self.xs, us)
            max_u = max(max_u, max(us))

        print(max_u)
        self.plot.plot([-self.a.get(), -self.a.get()], [-max_u, max_u], color='black')
        self.plot.plot([self.a.get(), self.a.get()], [-max_u, max_u], color='black')