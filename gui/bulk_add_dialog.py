import tkinter as tk
from tkinter import ttk, messagebox
import csv
from io import StringIO

class BulkAddDialog:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Bulk Add Materials")
        self.dialog.geometry("900x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        self.dialog.wait_window()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.LabelFrame(main_frame, text="Instructions", padding=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        instructions = (
            "Enter materials in CSV format (one per line):\n"
            "Format: Name, Brand, Type, Width, Height, Depth, Unit, Quantity, Color, Tutorial URL, Notes\n\n"
            "Example:\n"
            "Red Paper, BrandA, Paper, 20, 30, 0, cm, 5, Red, http://tutorial.com, Some notes\n"
            "Blue Fabric, BrandB, Fabric, 50, 100, 2, cm, 3, Blue, , Soft material"
        )
        
        ttk.Label(info_frame, text=instructions, justify=tk.LEFT).pack()
        
        text_frame = ttk.LabelFrame(main_frame, text="Material Data", padding=10)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.text_widget = tk.Text(text_frame, wrap=tk.NONE, width=80, height=20)
        
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        
        self.text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.text_widget.grid(row=0, column=0, sticky=tk.NSEW)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        h_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        box_frame = ttk.Frame(main_frame)
        box_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(box_frame, text="Assign all to Box (optional):").pack(side=tk.LEFT, padx=5)
        self.box_var = tk.StringVar()
        self.box_combo = ttk.Combobox(box_frame, textvariable=self.box_var, width=30, state="readonly")
        boxes = self.db.get_boxes()
        self.box_options = {"None": None}
        for box in boxes:
            self.box_options[box['name']] = box['id']
        self.box_combo['values'] = list(self.box_options.keys())
        self.box_combo.current(0)
        self.box_combo.pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Import", command=self.import_materials).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=5)
    
    def import_materials(self):
        text_content = self.text_widget.get("1.0", tk.END).strip()
        
        if not text_content:
            messagebox.showerror("Error", "Please enter material data")
            return
        
        box_name = self.box_var.get()
        box_id = self.box_options.get(box_name)
        
        lines = text_content.split('\n')
        success_count = 0
        error_count = 0
        errors = []
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                reader = csv.reader(StringIO(line))
                row = next(reader)
                
                if len(row) < 1:
                    errors.append(f"Line {line_num}: Empty line")
                    error_count += 1
                    continue
                
                name = row[0].strip() if len(row) > 0 else ""
                brand = row[1].strip() if len(row) > 1 else ""
                material_type = row[2].strip() if len(row) > 2 else ""
                width = float(row[3]) if len(row) > 3 and row[3].strip() else 0
                height = float(row[4]) if len(row) > 4 and row[4].strip() else 0
                depth = float(row[5]) if len(row) > 5 and row[5].strip() else 0
                unit = row[6].strip() if len(row) > 6 and row[6].strip() else "cm"
                quantity = int(row[7]) if len(row) > 7 and row[7].strip() else 1
                color = row[8].strip() if len(row) > 8 else ""
                tutorial_url = row[9].strip() if len(row) > 9 else ""
                notes = row[10].strip() if len(row) > 10 else ""
                
                if not name:
                    errors.append(f"Line {line_num}: Name is required")
                    error_count += 1
                    continue
                
                self.db.add_material(
                    name=name,
                    box_id=box_id,
                    brand=brand,
                    material_type=material_type,
                    width=width,
                    height=height,
                    depth=depth,
                    unit=unit,
                    quantity=quantity,
                    color=color,
                    tutorial_url=tutorial_url,
                    notes=notes
                )
                
                success_count += 1
                
            except Exception as e:
                errors.append(f"Line {line_num}: {str(e)}")
                error_count += 1
        
        result_msg = f"Import completed:\n{success_count} materials added successfully"
        
        if error_count > 0:
            result_msg += f"\n{error_count} errors occurred"
            if errors:
                result_msg += "\n\nErrors:\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    result_msg += f"\n... and {len(errors) - 10} more errors"
        
        if success_count > 0:
            self.result = success_count
            messagebox.showinfo("Import Results", result_msg)
            self.dialog.destroy()
        else:
            messagebox.showerror("Import Failed", result_msg)
    
    def cancel(self):
        self.dialog.destroy()
