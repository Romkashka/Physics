import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as backend_tkagg

import PageTemplate
import oscillator_calculations


class OscillatorPage(PageTemplate.Page):
    def __init__(self, *args, **kwargs):
        PageTemplate.Page.__init__(self, *args, **kwargs)

        self.fig = mpl.figure.Figure(dpi=125)
        self.axis = self.fig.add_subplot(111)

        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=3, column=1, columnspan=6)

        self.toolbar = backend_tkagg.NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.grid(row=4, column=1, columnspan=6)

        self.omega = tk.DoubleVar()
        self.omega.set(1e9)
        self.omega_label = ttk.Label(self, text="Natural frequency")
        self.omega_entry = ttk.Entry(self, width=10, textvariable=self.omega)
        self.omega_label.grid(row=1, column=1)
        self.omega_entry.grid(row=2, column=1)

        self.mass = tk.DoubleVar()
        self.mass.set(9e-31)
        self.mass_label = ttk.Label(self, text="Mass")
        self.mass_entry = ttk.Entry(self, width=10, textvariable=self.mass)
        self.mass_label.grid(row=1, column=2)
        self.mass_entry.grid(row=2, column=2)

        self.n = tk.IntVar()
        self.n.set(2)
        self.n_label = ttk.Label(self, text="Function number")
        self.n_entry = ttk.Entry(self, width=5, textvariable=self.n)
        self.n_label.grid(row=1, column=3)
        self.n_entry.grid(row=2, column=3)

        self.xs, self.ys, self.a, E= oscillator_calculations.calculate(self.mass.get(), self.omega.get(), self.n.get())
        self.function_line, = self.axis.plot(self.xs, self.ys)
        self.left_boundary_line, = self.axis.plot([-self.a, -self.a], [min(self.ys) * 1.1, max(self.ys) * 1.1], color='black')
        self.right_boundary_line, = self.axis.plot([self.a, self.a], [min(self.ys) * 1.1, max(self.ys) * 1.1], color='black')
        # plt.ion()
        plt.title("m = " + str(self.mass.get()) + ", $\omega$ = " + str(self.omega.get()) + ", n = " + str(
            self.n.get()) + ", E = " + str(E))

        self.simulate_label = ttk.Label(self, text="Simulate")
        self.simulate_button = ttk.Button(self, text="Run", command=self.simulate)
        self.simulate_label.grid(row=1, column=4)
        self.simulate_button.grid(row=2, column=4)

        self.save_images_label = ttk.Label(self, text="Save first k functions:")
        self.k = tk.IntVar()
        self.k.set(10)
        self.k_entry = ttk.Entry(self, width=5, textvariable=self.k)
        self.save_images_button = ttk.Button(self, text="Save", command=self.save_images)
        self.save_images_button.grid(row=2, column=5, columnspan=2)
        self.save_images_label.grid(row=1, column=5)
        self.k_entry.grid(row=1, column=6)

    def simulate(self):
        plt.ion()
        self.xs, self.ys, self.a, E = oscillator_calculations.calculate(self.mass.get(), self.omega.get(), self.n.get())
        self.axis.set_xlim([min(self.xs), max(self.xs)])
        self.axis.set_ylim([min(self.ys) * 1.1, max(self.ys) * 1.1])
        self.function_line.set_xdata(self.xs)
        self.function_line.set_ydata(self.ys)
        self.left_boundary_line.set_xdata([-self.a, -self.a])
        self.left_boundary_line.set_ydata([min(self.ys) * 1.1, max(self.ys) * 1.1])
        self.right_boundary_line.set_xdata([self.a, self.a])
        self.right_boundary_line.set_ydata([min(self.ys) * 1.1, max(self.ys) * 1.1])
        plt.title("m = " + str(self.mass.get()) + ", $\omega$ = " + str(self.omega.get()) + ", n = " + str(self.n.get()) + ", E = " + str(E))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.ioff()

    def save_images(self):
        plt.ioff()
        for i in range(0, self.k.get() + 1):
            self.draw_secretly(i)
        plt.ion()

    def draw_secretly(self, k):
        tmp_fig = plt.figure()
        tmp_plot = tmp_fig.add_subplot(111)
        xs, ys, a, E = oscillator_calculations.calculate(self.mass.get(), self.omega.get(), k)
        tmp_plot.plot(xs, ys)
        tmp_plot.plot([-a, -a], [min(ys) * 1.1, max(ys) * 1.1], color='black')
        tmp_plot.plot([a, a], [min(ys) * 1.1, max(ys) * 1.1], color='black')
        plt.title("m = " + str(self.mass.get()) + ", $\omega$ = " + str(self.omega.get()) + ", n = " + str(k) + ", E = " + str(E))
        plt.savefig("images\\oscillator_" + str(k), bbox_inches='tight')
