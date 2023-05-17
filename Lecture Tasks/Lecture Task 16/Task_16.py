import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from scipy.special import sph_harm


def getRadiiAndColor(values):
    Ymax, Ymin = values.max(), values.min()
    if (Ymax != Ymin):
        Yvals = 2 * (values - Ymin) / (Ymax - Ymin) - 1
        radii = np.abs(Yvals)
        colors = 0.5 * (Yvals + 1)
    else:
        radii = np.ones(values.shape)
        colors = np.ones(values.shape)
    return radii, colors


class Plotter:
    def __init__(self, l, m, f):
        self.l = l
        self.m = m
        self.f = f

    def print(self):
        theta = np.linspace(0, np.pi, 100)
        phi = np.linspace(0, 2 * np.pi, 100)
        theta, phi = np.meshgrid(theta, phi)

        values = self.f(theta, phi)

        radii, colors = getRadiiAndColor(values)
        # radii, colors = getRadiiAndColor(sph_harm(self.m, self.l, phi, theta).real)

        xs = radii * np.sin(theta) * np.cos(phi)
        ys = radii * np.sin(theta) * np.sin(phi)
        zs = radii * np.cos(theta)

        title = "l = " + str(self.l) + ", m = " + str(self.m)

        fig = plt.figure(figsize=plt.figaspect(1.))
        ax_real = fig.add_subplot(121, projection='3d')
        ax_real.plot_surface(xs, ys, zs, rstride=1, cstride=1, facecolors=cm.coolwarm(colors))
        ax_real.set_xlabel('X')
        ax_real.set_ylabel('Y')
        ax_real.set_zlabel('Z')
        ax_real.set_xlim(-1, 1)
        ax_real.set_ylim(-1, 1)
        ax_real.set_zlim(-1, 1)

        plt.title(title + " real")

        radii, colors = getRadiiAndColor(sph_harm(self.m, self.l, phi, theta).imag)

        xs = radii * np.sin(theta) * np.cos(phi)
        ys = radii * np.sin(theta) * np.sin(phi)
        zs = radii * np.cos(theta)

        ax_imaginary = fig.add_subplot(122, projection='3d')
        ax_imaginary.plot_surface(xs, ys, zs, rstride=1, cstride=1, facecolors=cm.coolwarm(colors))
        ax_imaginary.set_xlabel('X')
        ax_imaginary.set_ylabel('Y')
        ax_imaginary.set_zlabel('Z')
        ax_imaginary.set_xlim(-1, 1)
        ax_imaginary.set_ylim(-1, 1)
        ax_imaginary.set_zlim(-1, 1)

        plt.title(title + " imag")
        # plt.show()
        # fig.savefig("Task_19_1_y" + str(self.l) + str(self.m),bbox_inches='tight')

        print("\\begin{center}")
        print("    \\includegraphics*[width=0.8\\textwidth]{Task_19_1_y" + str(self.l) + str(self.m) + "}")
        print("\\end{center}")


Plotter(0, 0, lambda theta, phi: 0.5 * np.sqrt(1 / np.pi) * np.ones(theta.shape)).print()

Plotter(1, -1, lambda theta, phi: 0.5 * np.sqrt(3 / (2 * np.pi)) * np.cos(-phi) * np.sin(theta)).print()
Plotter(1, 0, lambda theta, phi: 0.5 * np.sqrt(3 / np.pi) * np.cos(theta)).print()
Plotter(1, 1, lambda theta, phi: 0.5 * np.sqrt(3 / (2 * np.pi)) * np.cos(phi) * np.sin(theta)).print()

Plotter(2, -2, lambda theta, phi: 0.25 * np.sqrt(15 / (2 * np.pi)) * np.cos(-2 * phi) * np.sin(theta) ** 2).print()
Plotter(2, -1,lambda theta, phi: 0.5 * np.sqrt(15 / (2 * np.pi)) * np.cos(-phi) * np.cos(theta) * np.sin(theta)).print()
Plotter(2, 0, lambda theta, phi: 0.25 * np.sqrt(5 / np.pi) * (3 * np.cos(theta) ** 2 - 1)).print()
Plotter(2, 1, lambda theta, phi: -0.5 * np.sqrt(15 / (2 * np.pi)) * np.cos(phi) * np.sin(theta) * np.cos(theta)).print()
Plotter(2, 2, lambda theta, phi: 0.25 * np.sqrt(15 / (2 * np.pi)) * np.cos(2 * phi) * np.sin(theta) ** 2).print()

Plotter(3, -3, lambda theta, phi: 0.125 * np.sqrt(35 / np.pi) * np.cos(-3 * phi) * np.sin(theta) ** 3).print()
Plotter(3, -2, lambda theta, phi: 0.25 * np.sqrt(105 / (2 * np.pi)) * np.cos(-2 * phi) * np.sin(theta) ** 2 * np.cos(theta)).print()
Plotter(3, -1, lambda theta, phi: 0.125 * np.sqrt(21 / np.pi) * np.cos(-phi) * np.sin(theta) * (5 * np.cos(theta) ** 2 - 1)).print()
Plotter(3, 0, lambda theta, phi: 0.25 * np.sqrt(7 / np.pi) * (5 * np.cos(theta) ** 3 - 3 * np.cos(theta))).print()
Plotter(3, 1, lambda theta, phi: -0.125 * np.sqrt(21 / np.pi) * np.cos(phi) * np.sin(theta) * (5 * np.cos(theta) ** 2 - 1)).print()
Plotter(3, 2, lambda theta, phi: 0.25 * np.sqrt(105 / (2 * np.pi)) * np.cos(2 * phi) * np.sin(theta) ** 2 * np.cos(theta)).print()
Plotter(3, 3, lambda theta, phi: -0.125 * np.sqrt(35 / np.pi) * np.cos(3 * phi) * np.sin(theta) ** 3).print()
