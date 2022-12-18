import numpy
import numpy as np

import common
from scipy.signal import argrelextrema


def modulate(carrier_freq, length, rate, sample_points, modulation_ratio):
    x, carrier = common.discretize_sine_wave(carrier_freq, length, rate)
    return carrier * (1 + modulation_ratio * sample_points)


def demodulate(signal):
    # print(signal)
    signal = np.abs(signal)
    maxima = np.array(argrelextrema(signal, np.greater)).flatten()
    print(maxima)
    if maxima[0] != 0:
        maxima = numpy.append([0], maxima)
    if maxima[len(maxima)-1] != len(signal) - 1:
        maxima = np.append(maxima, [len(signal) - 1])
    highs = signal[maxima]
    result = np.interp(np.linspace(0, 1, len(signal), endpoint=False), np.linspace(0, 1, len(highs), endpoint=False), highs) - 1
    return result
