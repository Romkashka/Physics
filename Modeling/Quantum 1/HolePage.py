import PageTemplate
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as backend_tkagg

import hole_calculations


class HolePage(PageTemplate.Page):
    def __init__(self, *args, **kwargs):
        PageTemplate.Page.__init__(self, *args, **kwargs)

        self.fig_hole = mpl.figure.Figure(dpi=125)
        self.plot = self.fig_hole.add_subplot(111)

        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig_hole, self)
        self.canvas.get_tk_widget().grid(row=3, column=1, columnspan=6)

        self.toolbar = backend_tkagg.NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.grid(row=4, column=1, columnspan=6)

        self.U = tk.DoubleVar()
        self.U.set(1.6e-19)
        self.U_label = ttk.Label(self, text="U")
        self.U_entry = ttk.Entry(self, width=10, textvariable=self.U)
        self.U_label.grid(row=1, column=1)
        self.U_entry.grid(row=2, column=1)

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

        self.simulate_label = ttk.Label(self, text="Simulate")
        self.simulate_button = ttk.Button(self, text="Run", command=self.simulate)
        self.simulate_label.grid(row=1, column=4)
        self.simulate_button.grid(row=2, column=4)

    def simulate(self):
        self.fig_hole = mpl.figure.Figure(dpi=125)
        self.plot = self.fig_hole.add_subplot(111)

        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig_hole, self)
        self.canvas.get_tk_widget().grid(row=3, column=1, columnspan=6)

        self.toolbar = backend_tkagg.NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.grid(row=4, column=1, columnspan=6)

        self.xs, self.uss, self.Es = hole_calculations.calculate(self.mass.get(), self.U.get(), self.a.get())
        max_u = 0
        for us in self.uss:
            self.plot.plot(self.xs, us)
            max_u = max(max_u, max(us))

        print(max_u)
        self.plot.plot([-self.a.get(), -self.a.get()], [-max_u, max_u], color='black')
        self.plot.plot([self.a.get(), self.a.get()], [-max_u, max_u], color='black')