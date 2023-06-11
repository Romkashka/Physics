import math
import numpy as np
import scipy.constants
from sympy import nsolve, Symbol, cot, sqrt, re
import hole_calculations


def calculate(m, a, omega_a, n):
    ka = Symbol('ka')
    even_eq = ka * cot(ka) + omega_a

    even_kas = np.sort(np.abs(hole_calculations.find_roots(ka, even_eq)))[:int(n/2)]
    odd_kas = np.arange(1, n+1, 2) * math.pi
    if omega_a > 28:
        even_kas = np.arange(1, n+1, 2) * math.pi

    even_ks = even_kas / a
    odd_ks = odd_kas / a

    omega = omega_a / a

    xs = np.linspace(-a, a, 100000)
    eps = xs[1] - xs[0]
    khi = math.sqrt(omega / eps)

    odd_xs = np.copy(xs)
    for i in range(int(len(odd_xs) / 2), len(odd_xs)):
        if odd_xs[i] > 0:
            odd_xs[i] -= 2 * a

    us = list()
    for k in odd_ks:
        A = math.sqrt(1 / a)
        us.append(A * np.sin(k * (odd_xs + a)))

    for k in even_ks:
        A = math.sqrt(2 * k / (2 * k * a - math.sin(2 * k * a)))
        B = (A * math.sin(k * (a - eps))) / (math.exp(khi * eps) + math.exp(-khi * eps))
        tmp = np.zeros(len(xs))
        for i in range(0, len(tmp)):
            if xs[i] < -eps:
                tmp[i] = A * math.sin(k * (xs[i] + a))
            if -eps <= xs[i] <= eps:
                tmp[i] = B * (math.exp(khi * xs[i]) + math.exp(-khi * xs[i]))
            if xs[i] > eps:
                tmp[i] = -A * math.sin(k * (xs[i] - a))
        us.append(tmp)

    return xs, us