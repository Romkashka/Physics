import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft2
from scipy.fftpack import fftshift

Lx = 4
Ly = 4
Nx = 8000
Ny = 8000
z = 1000

dx = Lx / Nx
dy = Ly / Ny

x = dx * (np.arange(Nx) - Nx // 2)
y = dy * (np.arange(Ny) - Ny // 2)
xx, yy = np.meshgrid(x, y)

Nx = int(Nx)
Ny = int(Ny)
Es = np.zeros((Ny, Nx))


def add_rect(Es, x0, y0, lx, ly):
    Es += np.select(
        [((xx > (x0 - lx / 2)) & (xx < (x0 + lx / 2))) & ((yy > (y0 - ly / 2)) & (yy < (y0 + ly / 2))), True], [1, 0])


def sub_rect(Es, x0, y0, lx, ly):
    Es -= np.select([((xx > (x0 - lx / 2)) & (xx < (x0 + lx / 2))) & (
            (yy > (y0 - ly / 2)) & (yy < (y0 + ly / 2))), True], [1, 0])


def add_circ(Es, x0, y0, r):
    Es += (xx - x0) ** 2 + (yy - y0) ** 2 < r ** 2


def sub_circ(Es, x0, y0, r):
    Es -= (xx - x0) ** 2 + (yy - y0) ** 2 < r ** 2


def carpet(Es, x0, y0, side):
    sub_side = side / 3
    if sub_side < dx:
        return
    print(sub_side)
    sub_rect(Es, x0, y0, sub_side, sub_side)
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i != 0 or j != 0:
                carpet(Es, x0 + sub_side * i, y0 + sub_side * j, sub_side)


mm = 1e-3

side = 27 * mm

# Uncomment needed

# Circle:

# add_circ(Es, 0, 0, 10 * mm)

# Rectangle:

# add_rect(Es, 0, 0, 20 * mm, 20 * mm)

# Fractal:

add_rect(Es, 0, 0, side, side)
carpet(Es, 0, 0, side)

wave_length = 640 * 1e-9
k = 2 * np.pi / wave_length


fft_c = fft2(Es * np.exp(1j * k / (2 * z) * (xx ** 2 + yy ** 2)))
c = fftshift(fft_c)
abs_c = np.absolute(c)

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.imshow(abs_c, cmap='gray')

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
abs_c = np.sqrt(abs_c)
ax2.imshow(abs_c, cmap='gray')

ax1.set_ylabel("y mm")
ax1.set_xlabel("x, mm")
ax2.set_xlabel("x, mm")
ax2.set_ylabel("y, mm")

plt.show()
