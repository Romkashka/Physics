import tkinter as tk
from tkinter import ttk
import Page_base
import common
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as backend_tkagg

import modulation


class Page1(Page_base.Page):
    def __init__(self, *args, **kwargs):
        Page_base.Page.__init__(self, *args, **kwargs)

        self.fig = mpl.figure.Figure(dpi=125)
        self.fig = plt.gcf()
        self.signal_plot = self.fig.add_subplot(221)
        self.carrier_plot = self.fig.add_subplot(222)
        self.modulated_plot = self.fig.add_subplot(223)
        self.demodulated_plot = self.fig.add_subplot(224)

        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

        self.toolbar = backend_tkagg.NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.grid(row=5, column=0, columnspan=2)

        self.sampling_freq = 192000
        self.x, self.signal = common.discretize_sine_wave(0, 10, self.sampling_freq)
        self.carrier_freq = 4000.0
        _, self.carrier = common.discretize_sine_wave(self.carrier_freq, 10, self.sampling_freq)
        self.modulated = modulation.modulate(self.carrier_freq, 10, self.sampling_freq, self.signal, 1)
        self.demodulated = modulation.demodulate(self.modulated)

        self.signal_line, = self.signal_plot.plot(self.x, self.signal)
        self.carrier_line, = self.carrier_plot.plot(self.x, self.carrier)
        self.modulated_line, = self.modulated_plot.plot(self.x, self.modulated)
        self.demodulated_line, = self.demodulated_plot.plot(np.linspace(0, 10, len(self.demodulated), endpoint=False), self.demodulated)
        plt.ion()
        self.Reset()

        self.main_text = ttk.Label(self, text="Add new sine wave:")
        self.main_text.grid(row=0)

        self.freq = tk.DoubleVar()
        self.freq_label = ttk.Label(self, text="Frequency")
        self.freq_entry = ttk.Entry(self, width=10, textvariable=self.freq)
        self.freq_label.grid(row=1, column=0)
        self.freq_entry.grid(row=2, column=0)

        self.ampl = tk.DoubleVar()
        self.ampl_label = ttk.Label(self, text="Amplitude")
        self.ampl_entry = ttk.Entry(self, width=10, textvariable=self.ampl)
        self.ampl_label.grid(row=1, column=1)
        self.ampl_entry.grid(row=2, column=1)

        self.add_button = ttk.Button(self, text="Add", command=lambda: self.Add_sine_wave(self.freq.get(), self.ampl.get()))
        self.add_button.grid(row=3, column=0)

        self.reset_button = ttk.Button(self, text="Reset", command=self.Reset)
        self.reset_button.grid(row=3, column=1)

    def Add_sine_wave(self, freq, ampl):
        _, new_signal = common.discretize_sine_wave(freq, 10, self.sampling_freq)
        self.signal += new_signal * ampl
        self.Redraw()
        self.signal_plot.set_ylim([-max(np.abs(self.signal)) * 1.1, max(np.abs(self.signal)) * 1.1])
        self.modulated_plot.set_ylim([-max(np.abs(self.modulated)) * 1.1, max(np.abs(self.modulated)) * 1.1])

    def Reset(self):
        self.x, self.signal = common.discretize_sine_wave(0, 10, self.sampling_freq)
        self.signal_plot.set_ylim([-1.1, 1.1])
        self.signal_plot.set_xlim([0, 0.01])
        self.carrier_plot.set_ylim([-1.1, 1.1])
        self.carrier_plot.set_xlim([0, 0.01])
        self.modulated_plot.set_ylim([-1.1, 1.1])
        self.modulated_plot.set_xlim([0, 0.01])
        self.demodulated_plot.set_ylim([-1.1, 1.1])
        self.demodulated_plot.set_xlim([0, 0.01])
        self.Redraw()

    def Redraw(self):
        # self.signal = self.signal / self.signal.max()
        self.modulated = modulation.modulate(self.carrier_freq, 10, self.sampling_freq, self.signal, 1)
        self.demodulated = modulation.demodulate(self.modulated)
        self.signal_line.set_ydata(self.signal)
        self.modulated_line.set_ydata(self.modulated)
        self.demodulated_line.set_ydata(self.demodulated)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()