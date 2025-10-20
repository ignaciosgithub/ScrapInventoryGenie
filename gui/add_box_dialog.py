import tkinter as tk
from tkinter import ttk, messagebox

class AddBoxDialog:
    def __init__(self, parent, db, box_id=None):
        self.parent = parent
        self.db = db
        self.box_id = box_id
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Box" if box_id else "Add Box")
        self.dialog.geometry("500x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        if box_id:
            self.load_box_data()
        
        self.dialog.wait_window()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Name:*", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(main_frame, text="Location:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.location_entry = ttk.Entry(main_frame, width=40)
        self.location_entry.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        ttk.Label(main_frame, text="Description:").grid(row=2, column=0, sticky=tk.NW, pady=10)
        self.description_text = tk.Text(main_frame, width=40, height=6)
        self.description_text.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=5)
    
    def load_box_data(self):
        box = self.db.get_box(self.box_id)
        if not box:
            return
        
        self.name_entry.insert(0, box['name'])
        self.location_entry.insert(0, box['location'] or "")
        self.description_text.insert("1.0", box['description'] or "")
    
    def save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Box name is required")
            return
        
        location = self.location_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        
        if self.box_id:
            self.db.update_box(self.box_id, name, location, description)
            self.result = self.box_id
        else:
            self.result = self.db.add_box(name, location, description)
        
        messagebox.showinfo("Success", "Box saved successfully")
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()
