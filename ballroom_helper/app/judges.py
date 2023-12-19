from tkinter import *
from tkinter import ttk

class JudgeWindow:
    def __init__(self, master):
        self.master = master


    def initialize(self):
        judges = ttk.Frame(self.master)

        values = ["Итоговая аттестация - 2023"]
        combo = ttk.Combobox(judges, values=values, state="readonly")
        combo.pack(anchor=NW, padx=6, pady=6)

        return judges