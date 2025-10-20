import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class MaterialDetailDialog:
    def __init__(self, parent, db, material_id):
        self.parent = parent
        self.db = db
        self.material_id = material_id
        self.current_image_index = 0
        self.images = []
        self.photo_images = []
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Material Details")
        self.dialog.geometry("800x700")
        self.dialog.transient(parent)
        
        self.create_widgets()
        self.load_material_data()
        
        self.dialog.wait_window()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        image_frame = ttk.LabelFrame(main_frame, text="Images", padding=10)
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
        
        details_frame = ttk.LabelFrame(main_frame, text="Details", padding=10)
        details_frame.pack(fill=tk.BOTH, pady=5)
        
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, height=15, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Close", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def load_material_data(self):
        material = self.db.get_material(self.material_id)
        if not material:
            return
        
        details = []
        details.append(f"Name: {material['name']}")
        details.append(f"ID: {material['id']}")
        
        if material['brand']:
            details.append(f"Brand: {material['brand']}")
        
        if material['material_type']:
            details.append(f"Type: {material['material_type']}")
        
        if material['box_id']:
            box = self.db.get_box(material['box_id'])
            if box:
                details.append(f"Box: {box['name']}")
                if box['location']:
                    details.append(f"Box Location: {box['location']}")
        
        dimensions = f"{material['width']}x{material['height']}"
        if material['depth']:
            dimensions += f"x{material['depth']}"
        dimensions += f" {material['unit']}"
        details.append(f"Dimensions: {dimensions}")
        
        details.append(f"Quantity: {material['quantity']}")
        
        if material['color']:
            details.append(f"Color: {material['color']}")
        
        status = "Used" if material['is_used'] else "Available"
        details.append(f"Status: {status}")
        
        if material['is_used'] and material['used_date']:
            details.append(f"Used Date: {material['used_date']}")
        
        if material['tutorial_url']:
            details.append(f"Tutorial URL: {material['tutorial_url']}")
        
        if material['notes']:
            details.append(f"\nNotes:\n{material['notes']}")
        
        details.append(f"\nCreated: {material['created_at']}")
        
        self.details_text.configure(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", "\n".join(details))
        self.details_text.configure(state=tk.DISABLED)
        
        self.images = self.db.get_material_images(self.material_id)
        
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
                
                max_width = 760
                max_height = 400
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
