import numpy as np


def discretize_sine_wave(frequency, length, rate):
    x = np.linspace(0, length, length * rate, endpoint=False)
    y = np.sin(2 * np.pi * x * frequency)
    return x, y