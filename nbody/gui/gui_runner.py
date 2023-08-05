from tkinter import ttk
from typing import NoReturn
from nbody.gui.window import MainWindow


def run_gui() -> NoReturn:  # type: ignore
    handle = MainWindow()

    text = "This is a main window of N-Body simulation engine"
    message = ttk.Label(handle, text=text).pack()

    handle.mainloop()
