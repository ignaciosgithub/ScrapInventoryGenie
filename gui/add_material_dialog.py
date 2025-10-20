import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import shutil
from datetime import datetime

class AddMaterialDialog:
    def __init__(self, parent, db, material_id=None):
        self.parent = parent
        self.db = db
        self.material_id = material_id
        self.result = None
        self.image_paths = []
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Material" if material_id else "Add Material")
        self.dialog.geometry("700x800")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        if material_id:
            self.load_material_data()
        
        self.dialog.wait_window()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        row = 0
        
        ttk.Label(scrollable_frame, text="Name:*", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(scrollable_frame, width=40)
        self.name_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(scrollable_frame, text="Brand:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.brand_entry = ttk.Entry(scrollable_frame, width=40)
        self.brand_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(scrollable_frame, text="Material Type:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.type_entry = ttk.Entry(scrollable_frame, width=40)
        self.type_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(scrollable_frame, text="Box:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.box_var = tk.StringVar()
        self.box_combo = ttk.Combobox(scrollable_frame, textvariable=self.box_var, width=37, state="readonly")
        boxes = self.db.get_boxes()
        self.box_options = {"None": None}
        for box in boxes:
            self.box_options[box['name']] = box['id']
        self.box_combo['values'] = list(self.box_options.keys())
        self.box_combo.current(0)
        self.box_combo.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        dim_frame = ttk.LabelFrame(scrollable_frame, text="Dimensions", padding=10)
        dim_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=10)
        row += 1
        
        ttk.Label(dim_frame, text="Width:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.width_entry = ttk.Entry(dim_frame, width=10)
        self.width_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(dim_frame, text="Height:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.height_entry = ttk.Entry(dim_frame, width=10)
        self.height_entry.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(dim_frame, text="Depth:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.depth_entry = ttk.Entry(dim_frame, width=10)
        self.depth_entry.grid(row=0, column=5, sticky=tk.W, padx=5)
        
        ttk.Label(dim_frame, text="Unit:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.unit_var = tk.StringVar(value="cm")
        unit_combo = ttk.Combobox(dim_frame, textvariable=self.unit_var, width=8, state="readonly")
        unit_combo['values'] = ["cm", "mm", "in", "m"]
        unit_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(scrollable_frame, text="Quantity:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.quantity_entry = ttk.Entry(scrollable_frame, width=10)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(scrollable_frame, text="Color:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.color_entry = ttk.Entry(scrollable_frame, width=40)
        self.color_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(scrollable_frame, text="Tutorial URL:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.tutorial_entry = ttk.Entry(scrollable_frame, width=40)
        self.tutorial_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(scrollable_frame, text="Notes:").grid(row=row, column=0, sticky=tk.NW, pady=5)
        self.notes_text = tk.Text(scrollable_frame, width=40, height=5)
        self.notes_text.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        image_frame = ttk.LabelFrame(scrollable_frame, text="Images", padding=10)
        image_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=10)
        row += 1
        
        btn_frame = ttk.Frame(image_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Add Images", command=self.add_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Images", command=self.clear_images).pack(side=tk.LEFT, padx=5)
        
        self.image_list = tk.Listbox(image_frame, height=5)
        self.image_list.pack(fill=tk.BOTH, expand=True, pady=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=5)
    
    def load_material_data(self):
        material = self.db.get_material(self.material_id)
        if not material:
            return
        
        self.name_entry.insert(0, material['name'])
        self.brand_entry.insert(0, material['brand'] or "")
        self.type_entry.insert(0, material['material_type'] or "")
        
        if material['box_id']:
            box = self.db.get_box(material['box_id'])
            if box:
                self.box_var.set(box['name'])
        
        self.width_entry.insert(0, str(material['width']))
        self.height_entry.insert(0, str(material['height']))
        self.depth_entry.insert(0, str(material['depth']))
        self.unit_var.set(material['unit'])
        
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, str(material['quantity']))
        
        self.color_entry.insert(0, material['color'] or "")
        self.tutorial_entry.insert(0, material['tutorial_url'] or "")
        self.notes_text.insert("1.0", material['notes'] or "")
        
        images = self.db.get_material_images(self.material_id)
        for img in images:
            self.image_paths.append(img['image_path'])
            self.image_list.insert(tk.END, os.path.basename(img['image_path']))
    
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
            messagebox.showerror("Error", "Name is required")
            return
        
        brand = self.brand_entry.get().strip()
        material_type = self.type_entry.get().strip()
        
        box_name = self.box_var.get()
        box_id = self.box_options.get(box_name)
        
        try:
            width = float(self.width_entry.get() or 0)
            height = float(self.height_entry.get() or 0)
            depth = float(self.depth_entry.get() or 0)
            quantity = int(self.quantity_entry.get() or 1)
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric values")
            return
        
        unit = self.unit_var.get()
        color = self.color_entry.get().strip()
        tutorial_url = self.tutorial_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        if self.material_id:
            self.db.update_material(
                self.material_id,
                name=name,
                brand=brand,
                material_type=material_type,
                box_id=box_id,
                width=width,
                height=height,
                depth=depth,
                unit=unit,
                quantity=quantity,
                color=color,
                tutorial_url=tutorial_url,
                notes=notes
            )
            material_id = self.material_id
        else:
            material_id = self.db.add_material(
                name=name,
                brand=brand,
                material_type=material_type,
                box_id=box_id,
                width=width,
                height=height,
                depth=depth,
                unit=unit,
                quantity=quantity,
                color=color,
                tutorial_url=tutorial_url,
                notes=notes
            )
        
        if not os.path.exists("images/materials"):
            os.makedirs("images/materials")
        
        for idx, img_path in enumerate(self.image_paths):
            if os.path.exists(img_path):
                ext = os.path.splitext(img_path)[1]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"material_{material_id}_{timestamp}_{idx}{ext}"
                new_path = os.path.join("images/materials", new_filename)
                
                if img_path != new_path:
                    shutil.copy2(img_path, new_path)
                
                existing_images = self.db.get_material_images(material_id)
                if img_path not in [img['image_path'] for img in existing_images]:
                    self.db.add_material_image(material_id, new_path, is_primary=(idx == 0))
        
        self.result = material_id
        messagebox.showinfo("Success", "Material saved successfully")
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()
