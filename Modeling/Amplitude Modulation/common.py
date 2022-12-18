import numpy as np


def discretize_sine_wave(frequency, length, points):
    x = np.linspace(0, length, points, endpoint=False)
    y = np.sin(2 * np.pi * x * frequency)
    return x, y