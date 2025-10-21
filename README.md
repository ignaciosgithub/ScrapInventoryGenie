# Scrap Inventory Genie

A comprehensive inventory management system for tracking scrap materials, boxes, and projects with a user-friendly GUI.

## Features

### Materials Management
- Add materials with detailed information (name, brand, type, dimensions, color, etc.)
- Upload multiple images per material
- Mark materials as used/available
- Bulk import materials via CSV format
- Search and filter materials by:
  - Name
  - Brand
  - Material type
  - Color
  - Dimensions (width, height, depth)
  - Status (used/available)
- View detailed material information with image gallery

### Box Management
- Create and organize boxes to store materials
- Assign materials to specific boxes
- Track box locations
- View all materials in a box

### Project Management
- Create projects and track materials used
- Add project images
- Link materials to projects with quantity tracking
- Mark projects as complete
- View project details with materials list and images

### Database
- Local SQLite database for data persistence
- Automatic image storage and organization
- Relational data structure for boxes, materials, and projects

## Installation

### Windows Users - Quick Start

**Option 1: Build Your Own Executable (Recommended)**

1. Download this repository (click "Code" → "Download ZIP")
2. Extract the ZIP file
3. Double-click `build_windows.bat` to automatically build the executable
4. Find the executable in the `dist` folder
5. Run `ScrapInventoryGenie.exe`

See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed instructions.

**Option 2: Run from Source**

### Prerequisites
- Python 3.7 or higher ([Download Python](https://www.python.org/downloads/))
- Windows OS (designed for Windows, but works on Linux/Mac)

### Setup Instructions

1. Clone or download this repository

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure tkinter is installed (usually comes with Python on Windows):
   - If not installed, download and install Python from python.org with the "tcl/tk and IDLE" option checked

4. Run the application:
```bash
python main.py
```

For detailed Windows setup instructions, see [WINDOWS_SETUP.md](WINDOWS_SETUP.md).

## Usage

### Adding a Material

1. Go to the "Materials" tab
2. Click "Add Material"
3. Fill in the material details:
   - Name (required)
   - Brand, Type, Color (optional)
   - Dimensions (width, height, depth)
   - Quantity
   - Tutorial URL
   - Notes
4. Add images by clicking "Add Images"
5. Select a box to store the material (optional)
6. Click "Save"

### Bulk Adding Materials

1. Go to the "Materials" tab
2. Click "Bulk Add"
3. Enter materials in CSV format:
   ```
   Name, Brand, Type, Width, Height, Depth, Unit, Quantity, Color, Tutorial URL, Notes
   ```
   Example:
   ```
   Red Paper, BrandA, Paper, 20, 30, 0, cm, 5, Red, http://tutorial.com, Some notes
   Blue Fabric, BrandB, Fabric, 50, 100, 2, cm, 3, Blue, , Soft material
   ```
4. Optionally select a box to assign all materials to
5. Click "Import"

### Searching Materials

1. Go to the "Materials" tab
2. Use the search filters:
   - Enter text in Name, Brand, Type, or Color fields
   - Set dimension ranges (min/max width, height)
   - Check/uncheck "Include Used" to filter by status
3. Click "Search"
4. Click "Clear" to reset filters

### Managing Boxes

1. Go to the "Boxes" tab
2. Click "Add Box" to create a new box
3. Enter box name, location, and description
4. Double-click a box to view its materials
5. Edit or delete boxes as needed

### Creating Projects

1. Go to the "Projects" tab
2. Click "New Project"
3. Enter project name and description
4. Add materials:
   - First, select a material in the "Materials" tab
   - Then click "Add Material" in the project dialog
   - Specify quantity used
5. Add project images
6. Click "Save"
7. Mark project as complete when finished

### Viewing Details

- Double-click any material, box, or project to view detailed information
- Use navigation buttons to browse through images
- View all associated data and relationships

## Database Structure

The application uses SQLite with the following tables:
- **boxes**: Storage containers for materials
- **materials**: Individual scrap materials with properties
- **material_images**: Images associated with materials
- **projects**: Project records
- **project_images**: Images associated with projects
- **project_materials**: Links materials to projects with quantities

## File Structure

```
ScrapInventoryGenie/
├── main.py                 # Application entry point
├── database.py             # Database operations
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── scrap_inventory.db     # SQLite database (created on first run)
├── images/                # Image storage directory
│   ├── materials/         # Material images
│   └── projects/          # Project images
└── gui/                   # GUI components
    ├── __init__.py
    ├── main_window.py
    ├── materials_tab.py
    ├── boxes_tab.py
    ├── projects_tab.py
    ├── add_material_dialog.py
    ├── add_box_dialog.py
    ├── add_project_dialog.py
    ├── bulk_add_dialog.py
    ├── material_detail_dialog.py
    └── project_detail_dialog.py
```

## Data Backup

The database file `scrap_inventory.db` contains all your data. To backup:
1. Close the application
2. Copy `scrap_inventory.db` to a safe location
3. Also backup the `images/` folder to preserve all images

To restore:
1. Close the application
2. Replace `scrap_inventory.db` with your backup
3. Replace the `images/` folder with your backup

## Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed
- Verify tkinter is available: `python -c "import tkinter"`
- Install Pillow: `pip install Pillow`

### Images not displaying
- Check that image files exist in the `images/` folder
- Ensure Pillow is installed correctly
- Verify image file formats are supported (JPG, PNG, GIF, BMP)

### Database errors
- Close all instances of the application
- Check file permissions on `scrap_inventory.db`
- If corrupted, restore from backup

## License

This project is provided as-is for personal and commercial use.

## Support

For issues or questions, please refer to the repository documentation.
