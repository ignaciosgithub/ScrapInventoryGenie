import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
from datetime import datetime

class AddProjectDialog:
    def __init__(self, parent, db, materials_tab, project_id=None):
        self.parent = parent
        self.db = db
        self.materials_tab = materials_tab
        self.project_id = project_id
        self.result = None
        self.image_paths = []
        self.selected_materials = []
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Project" if project_id else "New Project")
        self.dialog.geometry("900x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        if project_id:
            self.load_project_data()
        
        self.dialog.wait_window()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.LabelFrame(main_frame, text="Project Information", padding=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text="Name:*", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(info_frame, width=60)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Description:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.description_text = tk.Text(info_frame, width=60, height=4)
        self.description_text.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        materials_frame = ttk.LabelFrame(main_frame, text="Materials Used", padding=10)
        materials_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        btn_frame = ttk.Frame(materials_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Add Material", command=self.add_material).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove Material", command=self.remove_material).pack(side=tk.LEFT, padx=5)
        
        list_frame = ttk.Frame(materials_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Material ID", "Name", "Brand", "Type", "Quantity Used")
        self.materials_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", selectmode="browse", height=8)
        
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
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.materials_tree.yview)
        self.materials_tree.configure(yscrollcommand=scrollbar.set)
        
        self.materials_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        image_frame = ttk.LabelFrame(main_frame, text="Project Images", padding=10)
        image_frame.pack(fill=tk.X, pady=5)
        
        img_btn_frame = ttk.Frame(image_frame)
        img_btn_frame.pack(fill=tk.X)
        
        ttk.Button(img_btn_frame, text="Add Images", command=self.add_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(img_btn_frame, text="Clear Images", command=self.clear_images).pack(side=tk.LEFT, padx=5)
        
        self.image_list = tk.Listbox(image_frame, height=4)
        self.image_list.pack(fill=tk.BOTH, expand=True, pady=5)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=5)
    
    def load_project_data(self):
        project = self.db.get_project(self.project_id)
        if not project:
            return
        
        self.name_entry.insert(0, project['name'])
        self.description_text.insert("1.0", project['description'] or "")
        
        materials = self.db.get_project_materials(self.project_id)
        for mat in materials:
            self.selected_materials.append({
                'id': mat['id'],
                'material_id': mat['material_id'],
                'name': mat['name'],
                'brand': mat['brand'] or "",
                'material_type': mat['material_type'] or "",
                'quantity_used': mat['quantity_used']
            })
            
            self.materials_tree.insert("", tk.END, values=(
                mat['material_id'],
                mat['name'],
                mat['brand'] or "",
                mat['material_type'] or "",
                mat['quantity_used']
            ))
        
        images = self.db.get_project_images(self.project_id)
        for img in images:
            self.image_paths.append(img['image_path'])
            self.image_list.insert(tk.END, os.path.basename(img['image_path']))
    
    def add_material(self):
        material_id = self.materials_tab.get_selected_material_id()
        
        if not material_id:
            messagebox.showwarning("Warning", "Please select a material from the Materials tab first")
            return
        
        for mat in self.selected_materials:
            if mat['material_id'] == material_id:
                messagebox.showwarning("Warning", "This material is already added to the project")
                return
        
        material = self.db.get_material(material_id)
        if not material:
            messagebox.showerror("Error", "Material not found")
            return
        
        quantity_dialog = tk.Toplevel(self.dialog)
        quantity_dialog.title("Quantity Used")
        quantity_dialog.geometry("300x150")
        quantity_dialog.transient(self.dialog)
        quantity_dialog.grab_set()
        
        ttk.Label(quantity_dialog, text=f"How many units of '{material['name']}' were used?", wraplength=250).pack(pady=10)
        
        quantity_var = tk.IntVar(value=1)
        quantity_spinbox = ttk.Spinbox(quantity_dialog, from_=1, to=material['quantity'], textvariable=quantity_var, width=10)
        quantity_spinbox.pack(pady=10)
        
        def confirm_quantity():
            quantity = quantity_var.get()
            
            self.selected_materials.append({
                'id': None,
                'material_id': material['id'],
                'name': material['name'],
                'brand': material['brand'] or "",
                'material_type': material['material_type'] or "",
                'quantity_used': quantity
            })
            
            self.materials_tree.insert("", tk.END, values=(
                material['id'],
                material['name'],
                material['brand'] or "",
                material['material_type'] or "",
                quantity
            ))
            
            quantity_dialog.destroy()
        
        ttk.Button(quantity_dialog, text="OK", command=confirm_quantity).pack(pady=5)
        
        quantity_dialog.wait_window()
    
    def remove_material(self):
        selection = self.materials_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a material to remove")
            return
        
        item = self.materials_tree.item(selection[0])
        material_id = item['values'][0]
        
        self.selected_materials = [m for m in self.selected_materials if m['material_id'] != material_id]
        self.materials_tree.delete(selection[0])
    
    def add_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"), ("All files", "*.*")]
        )
        
        for file in files:
            self.image_paths.append(file)
            self.image_list.insert(tk.END, os.path.basename(file))
    
    def clear_images(self):
        self.image_paths.clear()
        self.image_list.delete(0, tk.END)
    
    def save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Project name is required")
            return
        
        description = self.description_text.get("1.0", tk.END).strip()
        
        if self.project_id:
            self.db.update_project(self.project_id, name, description)
            project_id = self.project_id
            
            existing_materials = self.db.get_project_materials(project_id)
            for mat in existing_materials:
                self.db.remove_project_material(mat['id'])
        else:
            project_id = self.db.add_project(name, description)
        
        for mat in self.selected_materials:
            self.db.add_project_material(project_id, mat['material_id'], mat['quantity_used'])
        
        if not os.path.exists("images/projects"):
            os.makedirs("images/projects")
        
        for idx, img_path in enumerate(self.image_paths):
            if os.path.exists(img_path):
                ext = os.path.splitext(img_path)[1]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"project_{project_id}_{timestamp}_{idx}{ext}"
                new_path = os.path.join("images/projects", new_filename)
                
                if img_path != new_path:
                    shutil.copy2(img_path, new_path)
                
                existing_images = self.db.get_project_images(project_id)
                if img_path not in [img['image_path'] for img in existing_images]:
                    self.db.add_project_image(project_id, new_path)
        
        self.result = project_id
        messagebox.showinfo("Success", "Project saved successfully")
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()
