# Windows Setup Guide

## Option 1: Run from Source (Recommended for Development)

### Prerequisites
- Python 3.7 or higher (download from [python.org](https://www.python.org/downloads/))
- Make sure to check "Add Python to PATH" during installation

### Installation Steps

1. Download or clone this repository

2. Open Command Prompt in the project folder

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## Option 2: Create Portable Executable

### Build Your Own Executable

1. Follow steps 1-3 from Option 1

2. Install PyInstaller:
```bash
pip install pyinstaller
```

3. Build the executable:
```bash
pyinstaller --clean --onefile --windowed --name ScrapInventoryGenie main.py
```

4. Find the executable in the `dist` folder

5. Create a portable package:
   - Create a new folder named `ScrapInventoryGenie-Portable`
   - Copy `dist/ScrapInventoryGenie.exe` to this folder
   - Copy `README.md` to this folder
   - The application will create its database and images folder automatically on first run

### Running the Portable Version

1. Double-click `ScrapInventoryGenie.exe`
2. The application will start and create necessary files
3. Your data is stored in:
   - `scrap_inventory.db` - Database file
   - `images/` - Folder for material and project images

## Troubleshooting

### "Python is not recognized"
- Reinstall Python and check "Add Python to PATH"
- Or manually add Python to your system PATH

### "No module named 'tkinter'"
- Tkinter comes with Python on Windows
- If missing, reinstall Python and ensure "tcl/tk and IDLE" is checked

### "ModuleNotFoundError"
- Run: `pip install -r requirements.txt`

### Application won't start
- Check if antivirus is blocking the executable
- Try running as administrator
- Check Windows Event Viewer for error details

### Images not displaying
- Ensure the `images` folder exists in the same directory as the executable
- Check that image files are not corrupted

## Data Backup

To backup your inventory:
1. Close the application
2. Copy these files to a safe location:
   - `scrap_inventory.db`
   - `images/` folder (entire folder)

To restore:
1. Close the application
2. Replace the files with your backup copies

## System Requirements

- Windows 7 or later
- 100 MB free disk space
- 512 MB RAM minimum
- Screen resolution: 1024x768 or higher recommended
