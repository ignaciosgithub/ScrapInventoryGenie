# Building Windows Executable

This document explains how to build a standalone Windows executable for Scrap Inventory Genie.

## Prerequisites

- Python 3.7 or higher
- PyInstaller (`pip install pyinstaller`)
- All dependencies installed (`pip install -r requirements.txt`)

## Building on Windows

1. Open Command Prompt or PowerShell in the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install pyinstaller
```

3. Build the executable:
```bash
pyinstaller build_windows.spec
```

4. The executable will be created in the `dist` folder as `ScrapInventoryGenie.exe`

## Building on Linux (Cross-platform)

Note: Building a Windows executable on Linux requires Wine and additional setup. It's recommended to build on Windows for best results.

If you must build on Linux:

1. Install Wine and PyInstaller
2. Run: `pyinstaller build_windows.spec`
3. The output may not be fully compatible with Windows

## Distribution

After building, create a distribution package:

1. Create a folder named `ScrapInventoryGenie-Portable`
2. Copy the following files:
   - `dist/ScrapInventoryGenie.exe`
   - `README.md`
   - Create an empty `images` folder
3. Zip the folder for distribution

## Running the Portable Version

Users can simply:
1. Extract the ZIP file
2. Double-click `ScrapInventoryGenie.exe`
3. The application will create a database file and images folder automatically

## Notes

- The executable is self-contained and includes Python and all dependencies
- First run may be slower as Windows scans the executable
- The database file (`scrap_inventory.db`) will be created in the same folder as the executable
- Images are stored in the `images` subfolder
