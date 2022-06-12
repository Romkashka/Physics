import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib import animation
import tkinter as tk
from tqdm import tqdm

master = tk.Tk()

filename = 'test.txt'
data_file = open(filename, 'r')

data_array = [float(i) for i in data_file.readline().split()]
m1, m2, m3, x1_0, y1_0, z1_0, x2_0, y2_0, z2_0, x3_0, y3_0, z3_0, vx1_0, vy1_0, vz1_0, vx2_0, vy2_0, vz2_0, vx3_0, vy3_0, vz3_0 = data_array
data_vars = [m1, m2, m3, x1_0, y1_0, z1_0, x2_0, y2_0, z2_0, x3_0, y3_0, z3_0, vx1_0, vy1_0, vz1_0, vx2_0, vy2_0, vz2_0,
             vx3_0, vy3_0, vz3_0]

days, hours, minutes, seconds, iters = [2000, 0, 0, 0, 1000]

m1_text = tk.IntVar()
m2_text = tk.IntVar()
m3_text = tk.IntVar()

x1_0_text = tk.IntVar()
y1_0_text = tk.IntVar()
z1_0_text = tk.IntVar()
x2_0_text = tk.IntVar()
y2_0_text = tk.IntVar()
z2_0_text = tk.IntVar()
x3_0_text = tk.IntVar()
y3_0_text = tk.IntVar()
z3_0_text = tk.IntVar()

vx1_0_text = tk.IntVar()
vy1_0_text = tk.IntVar()
vz1_0_text = tk.IntVar()
vx2_0_text = tk.IntVar()
vy2_0_text = tk.IntVar()
vz2_0_text = tk.IntVar()
vx3_0_text = tk.IntVar()
vy3_0_text = tk.IntVar()
vz3_0_text = tk.IntVar()

text_vars = [m1_text, m2_text, m3_text, x1_0_text, y1_0_text, z1_0_text, x2_0_text, y2_0_text, z2_0_text, x3_0_text,
             y3_0_text, z3_0_text,
             vx1_0_text, vy1_0_text, vz1_0_text, vx2_0_text, vy2_0_text, vz2_0_text, vx3_0_text, vy3_0_text, vz3_0_text]



def save_data():
    global data_file, data_fields, message_label, flag
    data_file.close()
    data_file = open(filename, 'w')
    for data_field in data_fields:
        data_file.write(data_field.get().strip())
        data_file.write(' ')


def update_quit():
    global data_array, master, data_file
    global m1, m2, m3, x1_0, y1_0, z1_0, x2_0, y2_0, z2_0, x3_0, y3_0, z3_0, vx1_0, vy1_0, vz1_0, vx2_0, vy2_0, vz2_0, \
        vx3_0, vy3_0, vz3_0, days__, hours__, minutes__, seconds__, iters__, days, hours, minutes, seconds, iters

    days = int(days__.get().strip())
    hours = int(hours__.get().strip())
    minutes = int(minutes__.get().strip())
    seconds = int(seconds__.get().strip())
    iters = int(iters__.get().strip())
    m1 = m1_text.get()
    m2 = m2_text.get()
    m3 = m3_text.get()
    x1_0 = x1_0_text.get()
    y1_0 = y1_0_text.get()
    z1_0 = z1_0_text.get()
    x2_0 = x2_0_text.get()
    y2_0 = y2_0_text.get()
    z2_0 = z2_0_text.get()
    x3_0 = x3_0_text.get()
    y3_0 = y3_0_text.get()
    z3_0 = z3_0_text.get()
    vx1_0 = vx1_0_text.get()
    vy1_0 = vy1_0_text.get()
    vz1_0 = vz1_0_text.get()
    vx2_0 = vx2_0_text.get()
    vy2_0 = vy2_0_text.get()
    vz2_0 = vz2_0_text.get()
    vx3_0 = vx3_0_text.get()
    vy3_0 = vy3_0_text.get()
    vz3_0 = vz3_0_text.get()
    master.destroy()


for i in range(len(text_vars)):
    text_vars[i].set(data_vars[i])

tk.Label(master, text="Masses").grid(row=1, column=3)
tk.Label(master, text="Coordinates").grid(row=3, column=3)
tk.Label(master, text="Speeds").grid(row=7, column=3)

m__1 = tk.Entry(master, textvariable=m1_text)
m__2 = tk.Entry(master, textvariable=m2_text)
m__3 = tk.Entry(master, textvariable=m3_text)

x__1_0 = tk.Entry(master, textvariable=x1_0_text)
y__1_0 = tk.Entry(master, textvariable=y1_0_text)
z__1_0 = tk.Entry(master, textvariable=z1_0_text)
x__2_0 = tk.Entry(master, textvariable=x2_0_text)
y__2_0 = tk.Entry(master, textvariable=y2_0_text)
z__2_0 = tk.Entry(master, textvariable=z2_0_text)
x__3_0 = tk.Entry(master, textvariable=x3_0_text)
y__3_0 = tk.Entry(master, textvariable=y3_0_text)
z__3_0 = tk.Entry(master, textvariable=z3_0_text)

vx__1_0 = tk.Entry(master, textvariable=vx1_0_text)
vy__1_0 = tk.Entry(master, textvariable=vy1_0_text)
vz__1_0 = tk.Entry(master, textvariable=vz1_0_text)
vx__2_0 = tk.Entry(master, textvariable=vx2_0_text)
vy__2_0 = tk.Entry(master, textvariable=vy2_0_text)
vz__2_0 = tk.Entry(master, textvariable=vz2_0_text)
vx__3_0 = tk.Entry(master, textvariable=vx3_0_text)
vy__3_0 = tk.Entry(master, textvariable=vy3_0_text)
vz__3_0 = tk.Entry(master, textvariable=vz3_0_text)

days__ = tk.Entry(master)
hours__ = tk.Entry(master)
minutes__ = tk.Entry(master)
seconds__ = tk.Entry(master)
iters__ = tk.Entry(master)

tk.Label(master, text="m1").grid(row=2, column=0)
m__1.grid(row=2, column=1)
tk.Label(master, text="m2").grid(row=2, column=2)
m__2.grid(row=2, column=3)
tk.Label(master, text="m3").grid(row=2, column=4)
m__3.grid(row=2, column=5)

tk.Label(master, text="x1").grid(row=4, column=0)
x__1_0.grid(row=4, column=1)
tk.Label(master, text="y1").grid(row=5, column=0)
y__1_0.grid(row=5, column=1)
tk.Label(master, text="z1").grid(row=6, column=0)
z__1_0.grid(row=6, column=1)
tk.Label(master, text="x2").grid(row=4, column=2)
x__2_0.grid(row=4, column=3)
tk.Label(master, text="y2").grid(row=5, column=2)
y__2_0.grid(row=5, column=3)
tk.Label(master, text="z2").grid(row=6, column=2)
z__2_0.grid(row=6, column=3)
tk.Label(master, text="x3").grid(row=4, column=4)
x__3_0.grid(row=4, column=5)
tk.Label(master, text="y3").grid(row=5, column=4)
y__3_0.grid(row=5, column=5)
tk.Label(master, text="z3").grid(row=6, column=4)
z__3_0.grid(row=6, column=5)

tk.Label(master, text="vx1").grid(row=8, column=0)
vx__1_0.grid(row=8, column=1)
tk.Label(master, text="vy1").grid(row=9, column=0)
vy__1_0.grid(row=9, column=1)
tk.Label(master, text="vz1").grid(row=10, column=0)
vz__1_0.grid(row=10, column=1)
tk.Label(master, text="vx2").grid(row=8, column=2)
vx__2_0.grid(row=8, column=3)
tk.Label(master, text="vy2").grid(row=9, column=2)
vy__2_0.grid(row=9, column=3)
tk.Label(master, text="vz2").grid(row=10, column=2)
vz__2_0.grid(row=10, column=3)
tk.Label(master, text="vx3").grid(row=8, column=4)
vx__3_0.grid(row=8, column=5)
tk.Label(master, text="vy2").grid(row=9, column=4)
vy__3_0.grid(row=9, column=5)
tk.Label(master, text="vz3").grid(row=10, column=4)
vz__3_0.grid(row=10, column=5)

tk.Label(master, text="Days, hours, minutes, seconds").grid(row=11, column=2, columnspan=4)
days__.grid(row=12, column=1)
hours__.grid(row=12, column=2)
minutes__.grid(row=12, column=3)
seconds__.grid(row=12, column=4)

tk.Label(master, text="Iters").grid(row=13, column=3)
iters__.grid(row=14, column=3)

data_fields = [m__1, m__2, m__3, x__1_0, y__1_0, z__1_0, x__2_0, y__2_0, z__2_0, x__3_0, y__3_0, z__3_0,
               vx__1_0, vy__1_0, vz__1_0, vx__2_0, vy__2_0, vz__2_0, vx__3_0, vy__3_0, vz__3_0, ]

tk.Button(master, text='Save', command=save_data).grid(row=14, column=1)
tk.Button(master, text='Go!!!!', command=update_quit).grid(row=14, column=5)

master.mainloop()

k = 1 / np.sqrt(6.67e-11  # Gravitational constant
                * 1.99e30  # Mass of Sun
                / 1.5e11 ** 3  # Astronomical unit
                )

time_to_simulate = seconds + minutes * 60 + hours * 60 * 60 + days * 24 * 60 * 60
dt = time_to_simulate / iters
years_per_step = dt / (60 * 60 * 24 * 365.25)
timing = dt / k * iters


def dSdt(t, S):
    x1, y1, z1, x2, y2, z2, x3, y3, z3, vx1, vy1, vz1, vx2, vy2, vz2, vx3, vy3, vz3 = S
    r12 = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    r13 = np.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2 + (z3 - z1) ** 2)
    r23 = np.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2 + (z2 - z3) ** 2)
    return [vx1,
            vy1,
            vz1,
            vx2,
            vy2,
            vz2,
            vx3,
            vy3,
            vz3,
            m2 / r12 ** 3 * (x2 - x1) + m3 / r13 ** 3 * (x3 - x1),  # mass 1
            m2 / r12 ** 3 * (y2 - y1) + m3 / r13 ** 3 * (y3 - y1),
            m2 / r12 ** 3 * (z2 - z1) + m3 / r13 ** 3 * (z3 - z1),

            m1 / r12 ** 3 * (x1 - x2) + m3 / r23 ** 3 * (x3 - x2),  # mass 2
            m1 / r12 ** 3 * (y1 - y2) + m3 / r23 ** 3 * (y3 - y2),
            m1 / r12 ** 3 * (z1 - z2) + m3 / r23 ** 3 * (z3 - z2),

            m1 / r13 ** 3 * (x1 - x3) + m2 / r23 ** 3 * (x2 - x3),  # mass 3
            m1 / r13 ** 3 * (y1 - y3) + m2 / r23 ** 3 * (y2 - y3),
            m1 / r13 ** 3 * (z1 - z3) + m2 / r23 ** 3 * (z2 - z3)
            ]


t = np.linspace(0, timing, iters)

sol = solve_ivp(dSdt, (0, timing),
                y0=[x1_0, y1_0, z1_0, x2_0, y2_0, z2_0, x3_0, y3_0, z3_0, vx1_0, vy1_0, vz1_0, vx2_0, vy2_0, vz2_0,
                    vx3_0, vy3_0, vz3_0],
                method='DOP853', t_eval=t, rtol=1e-10, atol=1e-13)

t = sol.t
x1 = sol.y[0]
y1 = sol.y[1]
z1 = sol.y[2]
x2 = sol.y[3]
y2 = sol.y[4]
z2 = sol.y[5]
x3 = sol.y[6]
y3 = sol.y[7]
z3 = sol.y[8]
vx1 = sol.y[9]
vy1 = sol.y[10]
vz1 = sol.y[11]
vx2 = sol.y[12]
vy2 = sol.y[13]
vz2 = sol.y[14]
vx3 = sol.y[15]
vy3 = sol.y[16]
vz3 = sol.y[17]
Ep = np.ndarray(iters)
Ek = np.ndarray(iters)
# print(k)

for i in range(iters):
    Ep[i] = -(6.67e-11 * m1 * m2 / np.sqrt((x2[i] - x1[i]) ** 2 + (y2[i] - y1[i]) ** 2 + (z2[i] - z1[i]) ** 2) / 1.5e11 * 1.99e30 ** 2 +
             6.67e-11 * m1 * m3 / np.sqrt((x3[i] - x1[i]) ** 2 + (y3[i] - y1[i]) ** 2 + (z3[i] - z1[i]) ** 2) / 1.5e11 * 1.99e30 ** 2 +
             6.67e-11 * m2 * m3 / np.sqrt((x3[i] - x2[i]) ** 2 + (y3[i] - y2[i]) ** 2 + (z3[i] - z2[i]) ** 2) / 1.5e11 * 1.99e30 ** 2)
    Ek[i] = (m1 / 2 * (vx1[i] ** 2 + vy1[i] ** 2 + vz1[i] ** 2) +
             m2 / 2 * (vx2[i] ** 2 + vy2[i] ** 2 + vz2[i] ** 2) +
             m3 / 2 * (vx3[i] ** 2 + vy3[i] ** 2 + vz3[i] ** 2)) * 1.99e30 * 1.5e11 ** 2 / k ** 2
    # print(Ek[i] - Ep[i])

# tt = 1 / np.sqrt(6.67e-11  # Gravitational constant
#                  * 1.99e30  # Mass of Sun
#                  / 1.5e11 ** 3  # Astronomical unit
#                  )
# print(tt)
# tt = tt / (60 * 60 * 24 * 365.25) * np.diff(t)[0]  # per time step (in years)
# print(np.diff(t)[0])


times = []
Ep_array = []
Ek_array = []
max_times = time_to_simulate / (60 * 60 * 24 * 365.25)
max_E = max(Ep.max(), Ek.max()) * 1.1
min_E = min(Ep.min(), Ek.min()) * 1.1


def animate(i):
    # ln1.set_data([x1[i], x2[i], x3[i]], [y1[i], y2[i], y3[i]])
    global iters
    ln1.set_data([x1[i]], [y1[i]])
    ln2.set_data([x2[i]], [y2[i]])
    ln3.set_data([x3[i]], [y3[i]])
    ln1.set_3d_properties([z1[i]])
    ln2.set_3d_properties([z2[i]])
    ln3.set_3d_properties([z3[i]])

    if i == 0:
        Ek_array.clear()
        Ep_array.clear()
        times.clear()
        ax2.clear()
        ax2.set_xlim(0, max_times)
        ax2.set_ylim(min_E, max_E)
        ax2.grid()
        # ax2.plot([0, max_times], 0, color='black')

    times.append(i * years_per_step)
    Ep_array.append(Ep[i])
    Ek_array.append(Ek[i])
    # axE1.clear()
    # axE2.clear()
    # axE3.lcear()
    ax2.plot(times, Ep_array, color='orange')
    ax2.plot(times, Ek_array, color='blue')
    ax2.plot([0, max_times], [0, 0], color='black')
    ax2.plot(times, np.array(Ek_array) + np.array(Ep_array), color='red')
    # text1.set_text('Time = {:.3f} Years'.format(i * years_per_step))


max_x = max(x1.max(), x2.max(), x3.max(), abs(x1.min()), abs(x2.min()), abs(x3.min()))
max_y = max(y1.max(), y2.max(), y3.max(), abs(y1.min()), abs(y2.min()), abs(y3.min()))
max_z = max(z1.max(), z2.max(), z3.max(), abs(z1.min()), abs(z2.min()), abs(z3.min()))

fig = plt.figure()
# ax1 = p3.Axes3D(fig)
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2)
ax1.grid()
ax2.grid()
ax2.set_xlim(0, max_times)
ax2.set_ylim(min_E, max_E)
ln1 = ax1.plot([], [], [], 'ro', lw=3, markersize=3)[0]
ln2 = ax1.plot([], [], [], 'bo', lw=3, markersize=3)[0]
ln3 = ax1.plot([], [], [], 'yo', lw=3, markersize=3)[0]
plt.subplots_adjust(top=0.9)
ax1.set_xlim3d(-max_x, max_x)
ax1.set_ylim3d(-max_y, max_y)
ax1.set_zlim3d(-max_z - 1, max_z + 1)
# ax2.set_xlim(-0.05, max_times)
# ax2.set_ylim(-0.05, max_E)
ani = animation.FuncAnimation(fig, animate, frames=tqdm(range(iters), colour="green"), interval=50)
ani.save('plan.gif', writer='pillow', fps=15)
plt.show()
