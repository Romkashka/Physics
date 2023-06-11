import math
import numpy as np
import scipy.constants
import scipy.special


def calculate(m, omega, n):
    E = scipy.constants.hbar * omega * (n + 0.5)
    k = math.sqrt(2 * m * E / scipy.constants.hbar ** 2)
    lambd = m * omega / scipy.constants.hbar

    x_max = math.sqrt(2 * E / (m * omega ** 2))

    xs = np.linspace(-x_max * 3, x_max * 3, 10000)
    ys = math.sqrt(1.0 / (2.0 ** n * math.factorial(n)) * math.sqrt(lambd / math.pi)) * \
         hermite(xs, m, omega, n) * np.exp(-0.5 * lambd * xs ** 2)

    return xs, ys, x_max, E


def hermite(x, m, omega, n):
    xs = np.sqrt(m * omega / scipy.constants.hbar) * x
    herm_coeffs = np.zeros(n + 1)
    herm_coeffs[n] = 1
    return np.polynomial.hermite.hermval(xs, herm_coeffs)
