import tkinter as tk
from tkinter import ttk, messagebox
from gui.materials_tab import MaterialsTab
from gui.boxes_tab import BoxesTab
from gui.projects_tab import ProjectsTab

class MainWindow:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        
        self.root.title("Scrap Inventory Genie")
        self.root.geometry("1200x800")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_menu()
        self.create_main_layout()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_layout(self):
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill=tk.X, side=tk.TOP)
        
        title_label = tk.Label(
            header, 
            text="Scrap Inventory Genie", 
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.materials_tab = MaterialsTab(self.notebook, self.db)
        self.boxes_tab = BoxesTab(self.notebook, self.db, self.materials_tab)
        self.projects_tab = ProjectsTab(self.notebook, self.db, self.materials_tab)
        
        self.notebook.add(self.materials_tab.frame, text="Materials")
        self.notebook.add(self.boxes_tab.frame, text="Boxes")
        self.notebook.add(self.projects_tab.frame, text="Projects")
    
    def show_about(self):
        messagebox.showinfo(
            "About Scrap Inventory Genie",
            "Scrap Inventory Genie v1.0\n\n"
            "A comprehensive inventory management system for tracking scrap materials, "
            "boxes, and projects.\n\n"
            "Features:\n"
            "- Track materials with images and detailed information\n"
            "- Organize materials in boxes\n"
            "- Create projects and track materials used\n"
            "- Search and filter materials\n"
            "- Mark materials as used\n"
            "- Bulk add materials"
        )
