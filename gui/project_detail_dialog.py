import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class ProjectDetailDialog:
    def __init__(self, parent, db, project_id):
        self.parent = parent
        self.db = db
        self.project_id = project_id
        self.current_image_index = 0
        self.images = []
        self.photo_images = []
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Project Details")
        self.dialog.geometry("900x750")
        self.dialog.transient(parent)
        
        self.create_widgets()
        self.load_project_data()
        
        self.dialog.wait_window()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        image_frame = ttk.LabelFrame(main_frame, text="Project Images", padding=10)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.image_label = tk.Label(image_frame, text="No images available", bg="gray90")
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        nav_frame = ttk.Frame(image_frame)
        nav_frame.pack(fill=tk.X, pady=5)
        
        self.prev_btn = ttk.Button(nav_frame, text="< Previous", command=self.prev_image)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.image_counter = ttk.Label(nav_frame, text="0 / 0")
        self.image_counter.pack(side=tk.LEFT, expand=True)
        
        self.next_btn = ttk.Button(nav_frame, text="Next >", command=self.next_image)
        self.next_btn.pack(side=tk.RIGHT, padx=5)
        
        details_frame = ttk.LabelFrame(main_frame, text="Project Information", padding=10)
        details_frame.pack(fill=tk.X, pady=5)
        
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, height=6, state=tk.DISABLED)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        materials_frame = ttk.LabelFrame(main_frame, text="Materials Used", padding=10)
        materials_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns = ("Material ID", "Name", "Brand", "Type", "Quantity Used")
        self.materials_tree = ttk.Treeview(materials_frame, columns=columns, show="tree headings", selectmode="browse", height=8)
        
        self.materials_tree.heading("#0", text="")
        self.materials_tree.column("#0", width=0, stretch=False)
        
        for col in columns:
            self.materials_tree.heading(col, text=col)
            if col == "Material ID":
                self.materials_tree.column(col, width=80)
            elif col == "Quantity Used":
                self.materials_tree.column(col, width=100)
            else:
                self.materials_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(materials_frame, orient=tk.VERTICAL, command=self.materials_tree.yview)
        self.materials_tree.configure(yscrollcommand=scrollbar.set)
        
        self.materials_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Close", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def load_project_data(self):
        project = self.db.get_project(self.project_id)
        if not project:
            return
        
        details = []
        details.append(f"Name: {project['name']}")
        details.append(f"ID: {project['id']}")
        
        if project['description']:
            details.append(f"\nDescription:\n{project['description']}")
        
        status = "Completed" if project['completed_at'] else "In Progress"
        details.append(f"\nStatus: {status}")
        
        if project['completed_at']:
            details.append(f"Completed: {project['completed_at']}")
        
        details.append(f"Created: {project['created_at']}")
        
        self.details_text.configure(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", "\n".join(details))
        self.details_text.configure(state=tk.DISABLED)
        
        materials = self.db.get_project_materials(self.project_id)
        for mat in materials:
            self.materials_tree.insert("", tk.END, values=(
                mat['material_id'],
                mat['name'],
                mat['brand'] or "",
                mat['material_type'] or "",
                mat['quantity_used']
            ))
        
        self.images = self.db.get_project_images(self.project_id)
        
        if self.images:
            self.current_image_index = 0
            self.display_current_image()
        else:
            self.image_counter.config(text="0 / 0")
            self.prev_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.DISABLED)
    
    def display_current_image(self):
        if not self.images or self.current_image_index >= len(self.images):
            return
        
        image_path = self.images[self.current_image_index]['image_path']
        
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                
                max_width = 860
                max_height = 350
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(img)
                self.photo_images.append(photo)
                
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo
            except Exception as e:
                self.image_label.config(text=f"Error loading image: {str(e)}")
        else:
            self.image_label.config(text=f"Image not found: {image_path}")
        
        self.image_counter.config(text=f"{self.current_image_index + 1} / {len(self.images)}")
        
        self.prev_btn.config(state=tk.NORMAL if self.current_image_index > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_image_index < len(self.images) - 1 else tk.DISABLED)
    
    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.display_current_image()
    
    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.display_current_image()
