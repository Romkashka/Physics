import numpy as np
from matplotlib import pyplot as plt
import scipy.fft as fft


def discretize_sine_wave(frequency):
    x = np.linspace(0, 1, 100000, endpoint=False)
    y = np.sin(2 * np.pi * x * frequency)
    return x, y


def make_figures(x, y):
    fig = plt.figure()
    plot1 = fig.add_subplot(2, 2, 1)
    normalized = np.int16(y / y.max() * 32767)
    plot1.plot(x[:1000], normalized[:1000])

    y_fourier = fft.rfft(normalized)
    x_fourier = fft.rfftfreq(100000, 1 / 100000)
    plot2 = fig.add_subplot(2, 2, 2)
    plot2.plot(x_fourier[:15000], np.abs(y_fourier)[:15000])

    tmp = len(x_fourier) / 50000
    y_fourier[int(tmp * 9000):] = 0
    plot3 = fig.add_subplot(2, 2, 3)
    plot3.plot(x_fourier[:15000], np.abs(y_fourier)[:15000])

    filtered = fft.irfft(y_fourier)
    plot4 = fig.add_subplot(2, 2, 4)
    plot4.plot(x[:1000], filtered[:1000])


x, nice_tone1 = discretize_sine_wave(400)
_, nice_tone2 = discretize_sine_wave(800)
_, nice_tone3 = discretize_sine_wave(500)
_, noise_tone1 = discretize_sine_wave(10000)
_, noise_tone2 = discretize_sine_wave(12000)

noise_tone = noise_tone1 * 0.2 + noise_tone2 * 0.1
mixed_tone = nice_tone1 + nice_tone2 + nice_tone3

make_figures(x, nice_tone1 + noise_tone)
make_figures(x, mixed_tone + noise_tone)

plt.show()