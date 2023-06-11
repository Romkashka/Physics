import math

import matplotlib.pyplot as plt
import numpy as np
import scipy.constants
from sympy import nsolve, Symbol, tan, sqrt, re


def find_roots(x, eq):
    results = np.array([])

    for i in range(1, 100):
        try:
            res = re(nsolve(eq, x, i, prec=10))
            if np.isin(res.evalf(), results, invert=True):
                results = np.append(results, [float(res.evalf())])
        except Exception as e:
            continue

    for i in range(101, 1000, 5):
        try:
            res = re(nsolve(eq, x, i, prec=10))
            if np.isin(res.evalf(), results, invert=True):
                results = np.append(results, [float(res.evalf())])
        except Exception as e:
            continue

    return results


def calculate(m, U, a):
    k0 = math.sqrt(U * 2 * m / (scipy.constants.hbar ** 2))
    C = k0 * a

    xs = np.linspace(-2.5 * a, 2.5 * a, 100000)

    ka = Symbol('ka')
    even_eq = tan(ka) - sqrt(C ** 2 - ka ** 2) / ka
    odd_eq = tan(ka) + ka / sqrt(C ** 2 - ka ** 2)

    even_kas = find_roots(ka, even_eq)
    odd_kas = find_roots(ka, odd_eq)

    even_ks = even_kas / a
    odd_ks = odd_kas / a

    outer_xs = np.copy(xs)
    for i in range(0, len(outer_xs)):
        if -a <= outer_xs[i] <= a:
            outer_xs[i] = a

    inner_xs = np.copy(xs)
    for i in range(0, len(inner_xs)):
        if -a > inner_xs[i] or inner_xs[i] > a:
            inner_xs[i] = a

    even_xis = np.sqrt(k0 ** 2 - even_ks ** 2)
    us = list()
    for i in range(0, len(even_xis)):
        A = math.sqrt(1 / (a + 1 / even_xis[i]))
        us.append(A * np.cos(even_ks[i] * inner_xs) * np.exp(even_xis[i] * -np.abs(a - np.abs(outer_xs))))

    odd_xis = np.sqrt(k0 ** 2 - odd_ks ** 2)
    for i in range(0, len(odd_xis)):
        A = math.sqrt(1 / (a + 1 / odd_xis[i]))
        us.append(
            A * np.sin(odd_ks[i] * inner_xs) * np.exp(odd_xis[i] * -np.abs(a - np.abs(outer_xs))) * np.sign(outer_xs))

    even_Es = - (scipy.constants.hbar ** 2 * even_xis ** 2) / (2 * m)
    odd_Es = - (scipy.constants.hbar ** 2 * odd_xis ** 2) / (2 * m)

    return xs, us, np.append(even_Es, odd_Es)
