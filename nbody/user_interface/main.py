from window import MainWindow
import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    handle = MainWindow()
    
    text = "This is a main window of N-Body simulation engine"
    message = ttk.Label(handle, text=text).pack()

    handle.mainloop()
