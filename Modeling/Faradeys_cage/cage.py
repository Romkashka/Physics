import math
import tkinter as tk
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as backend_tkagg


class Application(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.wm_title("Faraday cage")

        self.frame = tk.Frame(self.root)
        self.frame.grid(row=5, column=0, columnspan=5)

        self.fig = mpl.figure.Figure(dpi=125)

        self.sub_plt = self.fig.add_subplot(111)
        self.sub_plt.set_aspect('equal')
        self.fig = plt.gcf()
        self.sub_plt = self.fig.gca()
        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack()

        self.n, self.r, self.distance, self.charge = [tk.IntVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()]
        [self.n.set(12), self.r.set(0.1), self.distance.set(2.0), self.charge.set(2 * math.pi)]

        self.n_entry = tk.Entry(self.root, textvariable=self.n, width=3)
        self.n_label = tk.Label(self.root, text="Number of wires")
        self.n_label.grid(row=0)

        self.r_entry = tk.Entry(self.root, textvariable=self.r, width=3)
        self.r_label = tk.Label(self.root, text="Wire diameter")
        self.r_label.grid(row=1)

        self.distance_entry = tk.Entry(self.root, textvariable=self.distance, width=3)
        self.distance_label = tk.Label(self.root, text="Distance of charge from center of cage")
        self.distance_label.grid(row=2)

        self.charge_entry = tk.Entry(self.root, textvariable=self.charge, width=3)
        self.charge_label = tk.Label(self.root, text="Charge")
        self.charge_label.grid(row=3)

        self.n_entry.grid(row=0, column=1)
        self.r_entry.grid(row=1, column=1)
        self.distance_entry.grid(row=2, column=1)
        self.charge_entry.grid(row=3, column=1)

        self.plot_button = tk.Button(
            self.root,
            text="Go!!!",
            command=lambda: self.simulate(),
            width=10
        )
        self.plot_button.grid(row=0, column=2)

        # Add a quit button
        self.quit_button = tk.Button(
            master=self.root,
            text='Quit',
            command=self.quit,
            width=10
        )
        self.quit_button.grid(row=1, column=2)
        self.toolbar = backend_tkagg.NavigationToolbar2Tk(self.canvas, self.frame)

    def error(self, problem, message):
        self.popup = tk.Toplevel()
        self.label = tk.Label(
            self.popup,
            text=problem + ":\n" + message,
            height=10,
            width=50
        )
        self.label.pack()

    def check_input(self):
        if self.n_value < 3:
            self.error("Input error", "Amount of wires should be not less than 3")
            return False
        if self.r_value < 0:
            self.error("Input error", "Wire diameter should be positive")
            return False
        if 1 + self.r_value / 2 + 0.1 >= abs(self.distance_value):
            self.error("Input error", "Charge inside the cage")
            return False
        return True

    def simulate(self):
        self.n_value = self.n.get()
        self.r_value = self.r.get()
        self.distance_value = self.distance.get()
        self.charge_value = self.charge.get()
        self.sub_plt.cla()
        self.canvas.draw()
        if self.check_input():
            self.calculate()
            wires_roots = np.array([math.e ** (2j * math.pi * m / self.n_value) for m in range(1, self.n_value + 1)])
            for i in wires_roots:
                circle = plt.Circle((i.real, i.imag), self.r_value, color='blue')
                self.sub_plt.add_patch(circle)
            self.sub_plt.plot(self.distance_value.real, self.distance_value.imag, '.r')

            levels = np.arange(-2 * self.charge_value, 2 * self.charge_value, 0.1 * self.charge_value)
            contour_plot = self.sub_plt.contour(
                self.x_meshgrid,
                self.y_meshgrid,
                self.u_values,
                levels=levels,
                colors=('black'),
                corner_mask=True
            )
            self.sub_plt.clabel(contour_plot, inline=1, fontsize=10)
            min_u = self.u_values[500][int(3000 / (self.distance_value + 2.5))]
            max_u = self.u_values[500][0]
            print(min_u, max_u)
            for i in range(0, len(self.u_values)):
                for j in range(0, len(self.u_values)):
                    if self.u_values[i][j] > max_u:
                        self.u_values[i][j] = max_u
                    if self.u_values[i][j] < min_u:
                        self.u_values[i][j] = min_u
            self.sub_plt.pcolormesh(self.x_meshgrid, self.y_meshgrid, self.u_values)
            self.canvas.draw()

    def quit(self):
        self.root.quit()
        self.root.destroy()

    def calculate(self):
        np.set_printoptions(threshold=np.inf)
        wires_roots = np.array([math.e ** (2j * math.pi * m / self.n_value) for m in range(1, self.n_value + 1)])
        radii = self.r_value * np.ones(wires_roots.shape)
        N = int(max(0, round(4.0 + 0.5 * np.log10(self.r_value))))
        points_amount = 3 * N + 2
        circle_points = np.array([math.e ** (m * 2j * math.pi / points_amount) for m in range(1, points_amount + 1)])
        samples = [(wires_roots[i] + radii[i] * circle_points) for i in range(self.n_value)]
        samples_list = np.concatenate(samples)
        A = np.ndarray(shape=(len(samples_list) + 1, len(samples_list) + 1), dtype=float)
        for i in range(0, len(samples_list)):
            for j in range(0, len(samples_list)):
                if i == j:
                    A[i][j] = np.log(self.r_value / np.sqrt(points_amount))
                else:
                    A[i][j] = 1 * np.log(np.abs(samples_list[i] - samples_list[j]))
        for i in range(0, len(samples_list)):
            A[i][len(samples_list)] = 1
            A[len(samples_list)][i] = 1
        b = np.concatenate([-self.charge_value * np.log(np.abs(samples_list - self.distance_value)), np.zeros(1)])
        x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        x = np.delete(x, len(samples_list), axis=None)
        print(x)
        X = np.linspace(-1.5, 1.0 + self.distance_value, 1000)
        Y = np.linspace(-2.0, 2.0, 1000)
        [self.x_meshgrid, self.y_meshgrid] = np.meshgrid(X, Y)

        coordinates = self.x_meshgrid + 1j*self.y_meshgrid
        self.u_values = self.charge_value * np.log(np.abs(coordinates - self.distance_value))

        for i in range(0, len(x)):
            self.u_values = self.u_values + x[i] * np.log(np.abs(coordinates - samples_list[i]))
        for i in wires_roots:
            self.u_values[np.abs(coordinates - i) <= self.r_value] = np.nan

