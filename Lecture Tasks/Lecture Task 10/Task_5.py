import numpy as np
from matplotlib import pyplot as plt
import scipy.fft as fft

carrier_freq = 100
amplitude_source_freq = 5
amplitude_modulation_ratio = 0.5
phase_source_freq = 20
k_phi = 0.1
frequency_source_freq = 1
frequency_deviation = 40


def discretize_sine_wave(frequency):
    x = np.linspace(0, 1, 100000, endpoint=False)
    y = np.sin(2 * np.pi * x * frequency)
    return x, y


def make_figures(x, y):
    fig = plt.figure()
    plot1 = fig.add_subplot(2, 1, 1)
    normalized = y / y.max()
    plot1.plot(x, normalized)

    y_fourier = fft.rfft(normalized)
    x_fourier = fft.rfftfreq(100000, 1 / 100000)
    plot2 = fig.add_subplot(2, 1, 2)
    plot2.plot(x_fourier[:(2 * carrier_freq)], np.abs(y_fourier)[:(2 * carrier_freq)])


# Amplitude modulation

x, carrier = discretize_sine_wave(carrier_freq)
_, amplitude_source = discretize_sine_wave(amplitude_source_freq)

modulated = carrier * (1 + amplitude_modulation_ratio * amplitude_source)
make_figures(x, modulated)

# Phase modulation

x, phase_source = discretize_sine_wave(phase_source_freq)
phase_modulated = np.sin((2 * np.pi * carrier_freq) * x + (k_phi * 2 * np.pi) * phase_source)
phase_modulated_doubled = np.sin((2 * np.pi * carrier_freq) * x + (k_phi * 2 * np.pi) * phase_source * 2)

make_figures(x, phase_modulated)
make_figures(x, phase_modulated_doubled)

# Frequency modulation

x, frequency_source = discretize_sine_wave(frequency_source_freq)
y_freq_signal_1 = np.cos(2*np.pi*carrier_freq * x + frequency_deviation / frequency_source_freq * frequency_source)
y_freq_signal_2 = np.cos(2*np.pi*carrier_freq * x + frequency_deviation / 2 / frequency_source_freq * frequency_source)

make_figures(x, y_freq_signal_1)
make_figures(x, y_freq_signal_2)

plt.show()