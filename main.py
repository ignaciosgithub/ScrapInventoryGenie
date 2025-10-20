import tkinter as tk
from tkinter import ttk, messagebox
import os
from database import InventoryDatabase
from gui.main_window import MainWindow

def main():
    if not os.path.exists("images"):
        os.makedirs("images")
        os.makedirs("images/materials")
        os.makedirs("images/projects")
    
    db = InventoryDatabase()
    
    root = tk.Tk()
    app = MainWindow(root, db)
    root.mainloop()
    
    db.close()

if __name__ == "__main__":
    main()
