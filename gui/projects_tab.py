import tkinter as tk
from tkinter import ttk, messagebox
from gui.add_project_dialog import AddProjectDialog
from gui.project_detail_dialog import ProjectDetailDialog

class ProjectsTab:
    def __init__(self, parent, db, materials_tab):
        self.parent = parent
        self.db = db
        self.materials_tab = materials_tab
        self.frame = ttk.Frame(parent)
        self.current_projects = []
        
        self.create_widgets()
        self.load_projects()
    
    def create_widgets(self):
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="New Project", command=self.add_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit", command=self.edit_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete", command=self.delete_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="View Details", command=self.view_details).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Mark Complete", command=self.mark_complete).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self.load_projects).pack(side=tk.LEFT, padx=2)
        
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("ID", "Name", "Description", "Materials", "Created", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", selectmode="browse")
        
        self.tree.heading("#0", text="")
        self.tree.column("#0", width=0, stretch=False)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50)
            elif col == "Description":
                self.tree.column(col, width=300)
            elif col == "Materials":
                self.tree.column(col, width=80)
            elif col == "Status":
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<Double-1>", lambda e: self.view_details())
    
    def load_projects(self):
        self.tree.delete(*self.tree.get_children())
        self.current_projects = self.db.get_projects()
        
        for project in self.current_projects:
            materials = self.db.get_project_materials(project['id'])
            material_count = len(materials)
            
            description = project['description'][:50] + "..." if project['description'] and len(project['description']) > 50 else (project['description'] or "")
            
            status = "Completed" if project['completed_at'] else "In Progress"
            
            created = project['created_at'][:10] if project['created_at'] else ""
            
            self.tree.insert("", tk.END, values=(
                project['id'],
                project['name'],
                description,
                material_count,
                created,
                status
            ))
    
    def add_project(self):
        dialog = AddProjectDialog(self.frame, self.db, self.materials_tab)
        if dialog.result:
            self.load_projects()
    
    def edit_project(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a project to edit")
            return
        
        item = self.tree.item(selection[0])
        project_id = item['values'][0]
        
        dialog = AddProjectDialog(self.frame, self.db, self.materials_tab, project_id)
        if dialog.result:
            self.load_projects()
    
    def delete_project(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a project to delete")
            return
        
        item = self.tree.item(selection[0])
        project_id = item['values'][0]
        project_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete project '{project_name}'?"):
            self.db.delete_project(project_id)
            self.load_projects()
            messagebox.showinfo("Success", "Project deleted successfully")
    
    def view_details(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a project to view")
            return
        
        item = self.tree.item(selection[0])
        project_id = item['values'][0]
        
        ProjectDetailDialog(self.frame, self.db, project_id)
    
    def mark_complete(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a project to mark as complete")
            return
        
        item = self.tree.item(selection[0])
        project_id = item['values'][0]
        project_name = item['values'][1]
        status = item['values'][5]
        
        if status == "Completed":
            messagebox.showinfo("Info", "This project is already marked as completed")
            return
        
        if messagebox.askyesno("Mark Complete", f"Mark project '{project_name}' as completed?"):
            self.db.complete_project(project_id)
            self.load_projects()
            messagebox.showinfo("Success", "Project marked as completed")
