import tkinter as tk
from tkinter import ttk

import HolePage
import OscillatorPage
import WallPage


class Application(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.geometry("1200x900")
        self.root.wm_title("Schrödinger equation")

        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=tk.BOTH)
        self.frame1 = HolePage.HolePage(self.notebook)
        self.frame2 = OscillatorPage.OscillatorPage(self.notebook)
        self.frame3 = WallPage.WallPage(self.notebook)

        self.frame1.pack(expand=True, fill=tk.BOTH)
        self.frame2.pack(expand=True, fill=tk.BOTH)
        self.frame3.pack(expand=True, fill=tk.BOTH)

        self.notebook.add(self.frame1, text="Hole")
        self.notebook.add(self.frame2, text="Oscillator")
        self.notebook.add(self.frame3, text="Wall")


def main():
    root = tk.Tk()
    Application(root)
    tk.mainloop()


if __name__ == '__main__':
    main()