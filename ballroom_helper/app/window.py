from ballroom_helper.core.db.session import get_session
from ballroom_helper.app.registration import RegistrationWindow
from ballroom_helper.app.judges import JudgeWindow

from tkinter import *
from tkinter import ttk


class Root:
    def __init__(self) -> None:
        pass

    def initialize(self):
        root = Tk()
        root.title("BALLROOM_HELPER v.1.1")
        root.geometry("1500x1000")

        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=BOTH)

        main = RegistrationWindow(notebook).initialize()
        judges = JudgeWindow(notebook).initialize()

        notebook.add(main, text="Главная")
        notebook.add(judges, text="Судьи")

        root.mainloop()
