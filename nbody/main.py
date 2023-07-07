from window import MainWindow
import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    handle = MainWindow()
    
    message = ttk.Label(handle, text="Hello, World!").pack()

    handle.mainloop()
