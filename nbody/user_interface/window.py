from tkinter import *
from singleton import Singleton

class MainWindow(Tk, Singleton):
    def init(self):
        super().__init__()
    
    def __init__(self):
        self.title('N Body Simulations')
        self.geometry('1280x720')
        self.configure(bg='black')
        self.attributes('-alpha', 0.8)
        self.iconbitmap('nbody/assets/solar.ico')
