import tkinter as tk
from tkinter import ttk
from os.path import join as pjoin

import numpy as np
from scipy.io import wavfile
import os
import Page_base
import modulation


class Page2(Page_base.Page):
    def __init__(self, *args, **kwargs):
        Page_base.Page.__init__(self, *args, **kwargs)

        self.input_name = tk.StringVar()
        self.input_name_label = ttk.Label(self, text="Source file name (only .wav files allowed)")
        self.input_name_entry = ttk.Entry(self, width=40, textvariable=self.input_name)
        self.input_name_label.grid(row=1, column=0)
        self.input_name_entry.grid(row=2, column=0)

        self.output_name = tk.StringVar()
        self.output_name_label = ttk.Label(self, text="Result file name (only name, without format)")
        self.output_name_entry = ttk.Entry(self, width=40, textvariable=self.output_name)
        self.output_name_label.grid(row=1, column=1)
        self.output_name_entry.grid(row=2, column=1)

        self.carrier_freq = tk.DoubleVar()
        self.carrier_freq_label = ttk.Label(self, text="Carrier frequency")
        self.carrier_freq_entry = ttk.Entry(self, width=10, textvariable=self.carrier_freq)
        self.carrier_freq_label.grid(row=1, column=2)
        self.carrier_freq_entry.grid(row=2, column=2)

        self.run_button = ttk.Button(self, text="Run", command=self.Run)
        self.run_button.grid(row=3, column=1)

    def Run(self):
        wav_fname = pjoin(os.path.abspath(os.getcwd()), 'Samples', self.input_name.get())
        samplerate, data = wavfile.read(wav_fname)
        length = data.shape[0] / samplerate
        modulated = modulation.modulate(self.carrier_freq.get(), length, samplerate, data[:, 0], 1)
        demodulated1 = modulation.demodulate(modulated).astype(np.int16)
        if data.shape[1] == 2:
            modulated = modulation.modulate(self.carrier_freq.get(), length, samplerate, data[:, 1], 1)
            demodulated2 = modulation.demodulate(modulated).astype(np.int16)
            demodulated = np.vstack((demodulated1, demodulated2))
            demodulated = demodulated.transpose()
        else:
            demodulated = demodulated1
        name = self.output_name.get() + '.wav'
        wavfile.write(pjoin(os.path.abspath(os.getcwd()), 'Samples', name), samplerate, demodulated)



