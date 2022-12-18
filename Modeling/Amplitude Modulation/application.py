import tkinter as tk
from tkinter import ttk
import Page1
import Page2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as backend_tkagg


class Application(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.geometry("1080x700")
        self.root.wm_title("Amplitude modulation and demodulation")

        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=tk.BOTH)
        self.frame1 = Page1.Page1(self.notebook)
        self.frame2 = Page2.Page2(self.notebook)

        self.frame1.pack(expand=True, fill=tk.BOTH)
        self.frame2.pack(expand=True, fill=tk.BOTH)

        self.notebook.add(self.frame1, text="Python")
        self.notebook.add(self.frame2, text="Java")


def main():
    root = tk.Tk()
    Application(root)
    tk.mainloop()


if __name__ == '__main__':
    main()
