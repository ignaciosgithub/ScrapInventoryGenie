import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class InventoryDatabase:
    def __init__(self, db_path: str = "scrap_inventory.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS boxes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                box_id INTEGER,
                name TEXT NOT NULL,
                brand TEXT,
                material_type TEXT,
                width REAL,
                height REAL,
                depth REAL,
                unit TEXT DEFAULT 'cm',
                quantity INTEGER DEFAULT 1,
                color TEXT,
                tutorial_url TEXT,
                notes TEXT,
                is_used INTEGER DEFAULT 0,
                used_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (box_id) REFERENCES boxes (id) ON DELETE SET NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS material_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                material_id INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                is_primary INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (material_id) REFERENCES materials (id) ON DELETE CASCADE
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                material_id INTEGER NOT NULL,
                quantity_used INTEGER DEFAULT 1,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
                FOREIGN KEY (material_id) REFERENCES materials (id) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()
    
    def add_box(self, name: str, location: str = "", description: str = "") -> int:
        self.cursor.execute(
            "INSERT INTO boxes (name, location, description) VALUES (?, ?, ?)",
            (name, location, description)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_boxes(self) -> List[Dict]:
        self.cursor.execute("SELECT * FROM boxes ORDER BY name")
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_box(self, box_id: int) -> Optional[Dict]:
        self.cursor.execute("SELECT * FROM boxes WHERE id = ?", (box_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def update_box(self, box_id: int, name: str, location: str = "", description: str = ""):
        self.cursor.execute(
            "UPDATE boxes SET name = ?, location = ?, description = ? WHERE id = ?",
            (name, location, description, box_id)
        )
        self.conn.commit()
    
    def delete_box(self, box_id: int):
        self.cursor.execute("DELETE FROM boxes WHERE id = ?", (box_id,))
        self.conn.commit()
    
    def add_material(self, name: str, box_id: Optional[int] = None, brand: str = "", 
                    material_type: str = "", width: float = 0, height: float = 0, 
                    depth: float = 0, unit: str = "cm", quantity: int = 1, 
                    color: str = "", tutorial_url: str = "", notes: str = "") -> int:
        self.cursor.execute('''
            INSERT INTO materials (box_id, name, brand, material_type, width, height, 
                                 depth, unit, quantity, color, tutorial_url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (box_id, name, brand, material_type, width, height, depth, unit, 
              quantity, color, tutorial_url, notes))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_materials(self, box_id: Optional[int] = None, include_used: bool = True) -> List[Dict]:
        if box_id is not None:
            if include_used:
                self.cursor.execute("SELECT * FROM materials WHERE box_id = ? ORDER BY name", (box_id,))
            else:
                self.cursor.execute("SELECT * FROM materials WHERE box_id = ? AND is_used = 0 ORDER BY name", (box_id,))
        else:
            if include_used:
                self.cursor.execute("SELECT * FROM materials ORDER BY name")
            else:
                self.cursor.execute("SELECT * FROM materials WHERE is_used = 0 ORDER BY name")
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_material(self, material_id: int) -> Optional[Dict]:
        self.cursor.execute("SELECT * FROM materials WHERE id = ?", (material_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def update_material(self, material_id: int, **kwargs):
        allowed_fields = ['box_id', 'name', 'brand', 'material_type', 'width', 'height', 
                         'depth', 'unit', 'quantity', 'color', 'tutorial_url', 'notes']
        updates = []
        values = []
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = ?")
                values.append(value)
        
        if updates:
            values.append(material_id)
            query = f"UPDATE materials SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, values)
            self.conn.commit()
    
    def mark_material_used(self, material_id: int, used: bool = True):
        used_date = datetime.now().isoformat() if used else None
        self.cursor.execute(
            "UPDATE materials SET is_used = ?, used_date = ? WHERE id = ?",
            (1 if used else 0, used_date, material_id)
        )
        self.conn.commit()
    
    def delete_material(self, material_id: int):
        self.cursor.execute("DELETE FROM materials WHERE id = ?", (material_id,))
        self.conn.commit()
    
    def search_materials(self, name: str = "", brand: str = "", material_type: str = "",
                        min_width: float = 0, max_width: float = 0,
                        min_height: float = 0, max_height: float = 0,
                        min_depth: float = 0, max_depth: float = 0,
                        color: str = "", include_used: bool = True) -> List[Dict]:
        query = "SELECT * FROM materials WHERE 1=1"
        params = []
        
        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
        
        if brand:
            query += " AND brand LIKE ?"
            params.append(f"%{brand}%")
        
        if material_type:
            query += " AND material_type LIKE ?"
            params.append(f"%{material_type}%")
        
        if color:
            query += " AND color LIKE ?"
            params.append(f"%{color}%")
        
        if min_width > 0:
            query += " AND width >= ?"
            params.append(min_width)
        
        if max_width > 0:
            query += " AND width <= ?"
            params.append(max_width)
        
        if min_height > 0:
            query += " AND height >= ?"
            params.append(min_height)
        
        if max_height > 0:
            query += " AND height <= ?"
            params.append(max_height)
        
        if min_depth > 0:
            query += " AND depth >= ?"
            params.append(min_depth)
        
        if max_depth > 0:
            query += " AND depth <= ?"
            params.append(max_depth)
        
        if not include_used:
            query += " AND is_used = 0"
        
        query += " ORDER BY name"
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def add_material_image(self, material_id: int, image_path: str, is_primary: bool = False) -> int:
        if is_primary:
            self.cursor.execute(
                "UPDATE material_images SET is_primary = 0 WHERE material_id = ?",
                (material_id,)
            )
        
        self.cursor.execute(
            "INSERT INTO material_images (material_id, image_path, is_primary) VALUES (?, ?, ?)",
            (material_id, image_path, 1 if is_primary else 0)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_material_images(self, material_id: int) -> List[Dict]:
        self.cursor.execute(
            "SELECT * FROM material_images WHERE material_id = ? ORDER BY is_primary DESC, created_at",
            (material_id,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def delete_material_image(self, image_id: int):
        self.cursor.execute("DELETE FROM material_images WHERE id = ?", (image_id,))
        self.conn.commit()
    
    def add_project(self, name: str, description: str = "") -> int:
        self.cursor.execute(
            "INSERT INTO projects (name, description) VALUES (?, ?)",
            (name, description)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_projects(self) -> List[Dict]:
        self.cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_project(self, project_id: int) -> Optional[Dict]:
        self.cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def update_project(self, project_id: int, name: str, description: str = ""):
        self.cursor.execute(
            "UPDATE projects SET name = ?, description = ? WHERE id = ?",
            (name, description, project_id)
        )
        self.conn.commit()
    
    def complete_project(self, project_id: int):
        self.cursor.execute(
            "UPDATE projects SET completed_at = ? WHERE id = ?",
            (datetime.now().isoformat(), project_id)
        )
        self.conn.commit()
    
    def delete_project(self, project_id: int):
        self.cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.conn.commit()
    
    def add_project_image(self, project_id: int, image_path: str) -> int:
        self.cursor.execute(
            "INSERT INTO project_images (project_id, image_path) VALUES (?, ?)",
            (project_id, image_path)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_project_images(self, project_id: int) -> List[Dict]:
        self.cursor.execute(
            "SELECT * FROM project_images WHERE project_id = ? ORDER BY created_at",
            (project_id,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def delete_project_image(self, image_id: int):
        self.cursor.execute("DELETE FROM project_images WHERE id = ?", (image_id,))
        self.conn.commit()
    
    def add_project_material(self, project_id: int, material_id: int, quantity_used: int = 1) -> int:
        self.cursor.execute(
            "INSERT INTO project_materials (project_id, material_id, quantity_used) VALUES (?, ?, ?)",
            (project_id, material_id, quantity_used)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_project_materials(self, project_id: int) -> List[Dict]:
        self.cursor.execute('''
            SELECT pm.*, m.name, m.brand, m.material_type 
            FROM project_materials pm
            JOIN materials m ON pm.material_id = m.id
            WHERE pm.project_id = ?
        ''', (project_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def remove_project_material(self, project_material_id: int):
        self.cursor.execute("DELETE FROM project_materials WHERE id = ?", (project_material_id,))
        self.conn.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()
