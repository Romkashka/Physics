import numpy
import numpy as np

import common
from scipy.signal import argrelextrema


def modulate(carrier_freq, length, rate, sample_points, modulation_ratio):
    x, carrier = common.discretize_sine_wave(carrier_freq, length, len(sample_points))
    return carrier * ((sample_points.max() if sample_points.max() != 0 else 1) + modulation_ratio * sample_points)


def demodulate(signal):
    signal = np.abs(signal)
    maxima = np.array(argrelextrema(signal, np.greater)).flatten()
    if maxima[0] != 0:
        maxima = numpy.append([0], maxima)
    if maxima[len(maxima)-1] != len(signal) - 1:
        maxima = np.append(maxima, [len(signal) - 1])
    highs = signal[maxima]
    result = np.interp(np.linspace(0, 1, len(signal), endpoint=False), np.linspace(0, 1, len(highs), endpoint=False), highs)
    return result - result.max() / 2
