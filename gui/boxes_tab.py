import tkinter as tk
from tkinter import ttk, messagebox
from gui.add_box_dialog import AddBoxDialog

class BoxesTab:
    def __init__(self, parent, db, materials_tab):
        self.parent = parent
        self.db = db
        self.materials_tab = materials_tab
        self.frame = ttk.Frame(parent)
        self.current_boxes = []
        
        self.create_widgets()
        self.load_boxes()
    
    def create_widgets(self):
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Add Box", command=self.add_box).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit", command=self.edit_box).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete", command=self.delete_box).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="View Materials", command=self.view_materials).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self.load_boxes).pack(side=tk.LEFT, padx=2)
        
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("ID", "Name", "Location", "Description", "Material Count", "Created")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", selectmode="browse")
        
        self.tree.heading("#0", text="")
        self.tree.column("#0", width=0, stretch=False)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50)
            elif col == "Description":
                self.tree.column(col, width=300)
            elif col == "Material Count":
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<Double-1>", lambda e: self.view_materials())
    
    def load_boxes(self):
        self.tree.delete(*self.tree.get_children())
        self.current_boxes = self.db.get_boxes()
        
        for box in self.current_boxes:
            materials = self.db.get_materials(box_id=box['id'])
            material_count = len(materials)
            
            description = box['description'][:50] + "..." if box['description'] and len(box['description']) > 50 else (box['description'] or "")
            
            created = box['created_at'][:10] if box['created_at'] else ""
            
            self.tree.insert("", tk.END, values=(
                box['id'],
                box['name'],
                box['location'] or "",
                description,
                material_count,
                created
            ))
    
    def add_box(self):
        dialog = AddBoxDialog(self.frame, self.db)
        if dialog.result:
            self.load_boxes()
    
    def edit_box(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a box to edit")
            return
        
        item = self.tree.item(selection[0])
        box_id = item['values'][0]
        
        dialog = AddBoxDialog(self.frame, self.db, box_id)
        if dialog.result:
            self.load_boxes()
    
    def delete_box(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a box to delete")
            return
        
        item = self.tree.item(selection[0])
        box_id = item['values'][0]
        box_name = item['values'][1]
        material_count = item['values'][4]
        
        if material_count > 0:
            if not messagebox.askyesno("Confirm Delete", 
                f"Box '{box_name}' contains {material_count} materials. "
                "Materials will not be deleted but will be unassigned from this box. Continue?"):
                return
        else:
            if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete box '{box_name}'?"):
                return
        
        self.db.delete_box(box_id)
        self.load_boxes()
        messagebox.showinfo("Success", "Box deleted successfully")
    
    def view_materials(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a box to view its materials")
            return
        
        item = self.tree.item(selection[0])
        box_id = item['values'][0]
        box_name = item['values'][1]
        
        materials = self.db.get_materials(box_id=box_id)
        
        detail_dialog = tk.Toplevel(self.frame)
        detail_dialog.title(f"Materials in Box: {box_name}")
        detail_dialog.geometry("900x600")
        detail_dialog.transient(self.frame)
        
        main_frame = ttk.Frame(detail_dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Box: {box_name}", font=("Arial", 14, "bold")).pack(pady=10)
        
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Name", "Brand", "Type", "Dimensions", "Quantity", "Color", "Status")
        tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", selectmode="browse")
        
        tree.heading("#0", text="")
        tree.column("#0", width=0, stretch=False)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "ID":
                tree.column(col, width=50)
            elif col == "Dimensions":
                tree.column(col, width=120)
            elif col == "Quantity":
                tree.column(col, width=70)
            elif col == "Status":
                tree.column(col, width=80)
            else:
                tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for material in materials:
            dimensions = f"{material['width']}x{material['height']}"
            if material['depth']:
                dimensions += f"x{material['depth']}"
            dimensions += f" {material['unit']}"
            
            status = "Used" if material['is_used'] else "Available"
            
            tree.insert("", tk.END, values=(
                material['id'],
                material['name'],
                material['brand'] or "",
                material['material_type'] or "",
                dimensions,
                material['quantity'],
                material['color'] or "",
                status
            ))
        
        button_frame = ttk.Frame(detail_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Close", command=detail_dialog.destroy).pack(side=tk.RIGHT, padx=5)
