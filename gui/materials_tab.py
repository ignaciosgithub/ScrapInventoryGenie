import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import shutil
from datetime import datetime
from gui.add_material_dialog import AddMaterialDialog
from gui.bulk_add_dialog import BulkAddDialog
from gui.material_detail_dialog import MaterialDetailDialog

class MaterialsTab:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.frame = ttk.Frame(parent)
        self.current_materials = []
        
        self.create_widgets()
        self.load_materials()
    
    def create_widgets(self):
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Add Material", command=self.add_material).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Bulk Add", command=self.bulk_add).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit", command=self.edit_material).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete", command=self.delete_material).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Mark as Used", command=self.mark_used).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="View Details", command=self.view_details).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self.load_materials).pack(side=tk.LEFT, padx=2)
        
        search_frame = ttk.LabelFrame(self.frame, text="Search & Filter", padding=10)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        row1 = ttk.Frame(search_frame)
        row1.pack(fill=tk.X, pady=2)
        
        ttk.Label(row1, text="Name:").pack(side=tk.LEFT, padx=2)
        self.search_name = ttk.Entry(row1, width=15)
        self.search_name.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(row1, text="Brand:").pack(side=tk.LEFT, padx=2)
        self.search_brand = ttk.Entry(row1, width=15)
        self.search_brand.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(row1, text="Type:").pack(side=tk.LEFT, padx=2)
        self.search_type = ttk.Entry(row1, width=15)
        self.search_type.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(row1, text="Color:").pack(side=tk.LEFT, padx=2)
        self.search_color = ttk.Entry(row1, width=15)
        self.search_color.pack(side=tk.LEFT, padx=2)
        
        row2 = ttk.Frame(search_frame)
        row2.pack(fill=tk.X, pady=2)
        
        ttk.Label(row2, text="Width (cm):").pack(side=tk.LEFT, padx=2)
        self.search_min_width = ttk.Entry(row2, width=8)
        self.search_min_width.pack(side=tk.LEFT, padx=2)
        ttk.Label(row2, text="to").pack(side=tk.LEFT, padx=2)
        self.search_max_width = ttk.Entry(row2, width=8)
        self.search_max_width.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(row2, text="Height (cm):").pack(side=tk.LEFT, padx=2)
        self.search_min_height = ttk.Entry(row2, width=8)
        self.search_min_height.pack(side=tk.LEFT, padx=2)
        ttk.Label(row2, text="to").pack(side=tk.LEFT, padx=2)
        self.search_max_height = ttk.Entry(row2, width=8)
        self.search_max_height.pack(side=tk.LEFT, padx=2)
        
        self.include_used_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(row2, text="Include Used", variable=self.include_used_var).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(row2, text="Search", command=self.search_materials).pack(side=tk.LEFT, padx=5)
        ttk.Button(row2, text="Clear", command=self.clear_search).pack(side=tk.LEFT, padx=2)
        
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("ID", "Name", "Brand", "Type", "Dimensions", "Quantity", "Color", "Box", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", selectmode="browse")
        
        self.tree.heading("#0", text="")
        self.tree.column("#0", width=0, stretch=False)
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            if col == "ID":
                self.tree.column(col, width=50)
            elif col == "Dimensions":
                self.tree.column(col, width=120)
            elif col == "Quantity":
                self.tree.column(col, width=70)
            elif col == "Status":
                self.tree.column(col, width=80)
            else:
                self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<Double-1>", lambda e: self.view_details())
    
    def load_materials(self):
        self.tree.delete(*self.tree.get_children())
        self.current_materials = self.db.get_materials()
        
        for material in self.current_materials:
            box_name = ""
            if material['box_id']:
                box = self.db.get_box(material['box_id'])
                if box:
                    box_name = box['name']
            
            dimensions = f"{material['width']}x{material['height']}"
            if material['depth']:
                dimensions += f"x{material['depth']}"
            dimensions += f" {material['unit']}"
            
            status = "Used" if material['is_used'] else "Available"
            
            self.tree.insert("", tk.END, values=(
                material['id'],
                material['name'],
                material['brand'] or "",
                material['material_type'] or "",
                dimensions,
                material['quantity'],
                material['color'] or "",
                box_name,
                status
            ))
    
    def search_materials(self):
        name = self.search_name.get().strip()
        brand = self.search_brand.get().strip()
        material_type = self.search_type.get().strip()
        color = self.search_color.get().strip()
        
        min_width = 0
        max_width = 0
        min_height = 0
        max_height = 0
        
        try:
            if self.search_min_width.get().strip():
                min_width = float(self.search_min_width.get())
            if self.search_max_width.get().strip():
                max_width = float(self.search_max_width.get())
            if self.search_min_height.get().strip():
                min_height = float(self.search_min_height.get())
            if self.search_max_height.get().strip():
                max_height = float(self.search_max_height.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid dimension values")
            return
        
        include_used = self.include_used_var.get()
        
        self.current_materials = self.db.search_materials(
            name=name,
            brand=brand,
            material_type=material_type,
            color=color,
            min_width=min_width,
            max_width=max_width,
            min_height=min_height,
            max_height=max_height,
            include_used=include_used
        )
        
        self.tree.delete(*self.tree.get_children())
        
        for material in self.current_materials:
            box_name = ""
            if material['box_id']:
                box = self.db.get_box(material['box_id'])
                if box:
                    box_name = box['name']
            
            dimensions = f"{material['width']}x{material['height']}"
            if material['depth']:
                dimensions += f"x{material['depth']}"
            dimensions += f" {material['unit']}"
            
            status = "Used" if material['is_used'] else "Available"
            
            self.tree.insert("", tk.END, values=(
                material['id'],
                material['name'],
                material['brand'] or "",
                material['material_type'] or "",
                dimensions,
                material['quantity'],
                material['color'] or "",
                box_name,
                status
            ))
    
    def clear_search(self):
        self.search_name.delete(0, tk.END)
        self.search_brand.delete(0, tk.END)
        self.search_type.delete(0, tk.END)
        self.search_color.delete(0, tk.END)
        self.search_min_width.delete(0, tk.END)
        self.search_max_width.delete(0, tk.END)
        self.search_min_height.delete(0, tk.END)
        self.search_max_height.delete(0, tk.END)
        self.include_used_var.set(True)
        self.load_materials()
    
    def add_material(self):
        dialog = AddMaterialDialog(self.frame, self.db)
        if dialog.result:
            self.load_materials()
    
    def bulk_add(self):
        dialog = BulkAddDialog(self.frame, self.db)
        if dialog.result:
            self.load_materials()
    
    def edit_material(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a material to edit")
            return
        
        item = self.tree.item(selection[0])
        material_id = item['values'][0]
        
        dialog = AddMaterialDialog(self.frame, self.db, material_id)
        if dialog.result:
            self.load_materials()
    
    def delete_material(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a material to delete")
            return
        
        item = self.tree.item(selection[0])
        material_id = item['values'][0]
        material_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{material_name}'?"):
            self.db.delete_material(material_id)
            self.load_materials()
            messagebox.showinfo("Success", "Material deleted successfully")
    
    def mark_used(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a material to mark as used")
            return
        
        item = self.tree.item(selection[0])
        material_id = item['values'][0]
        material_name = item['values'][1]
        current_status = item['values'][8]
        
        if current_status == "Used":
            if messagebox.askyesno("Mark as Available", f"Mark '{material_name}' as available again?"):
                self.db.mark_material_used(material_id, False)
                self.load_materials()
                messagebox.showinfo("Success", "Material marked as available")
        else:
            if messagebox.askyesno("Mark as Used", f"Mark '{material_name}' as used?"):
                self.db.mark_material_used(material_id, True)
                self.load_materials()
                messagebox.showinfo("Success", "Material marked as used")
    
    def view_details(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a material to view")
            return
        
        item = self.tree.item(selection[0])
        material_id = item['values'][0]
        
        MaterialDetailDialog(self.frame, self.db, material_id)
    
    def sort_by_column(self, col):
        pass
    
    def get_selected_material_id(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            return item['values'][0]
        return None
