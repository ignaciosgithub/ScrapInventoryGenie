@echo off
echo ========================================
echo Scrap Inventory Genie - Windows Builder
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo.

echo Building executable...
pyinstaller --clean --onefile --windowed --name ScrapInventoryGenie main.py
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)
echo.

echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo The executable is located at: dist\ScrapInventoryGenie.exe
echo.
echo To create a portable package:
echo 1. Create a folder named "ScrapInventoryGenie-Portable"
echo 2. Copy dist\ScrapInventoryGenie.exe to that folder
echo 3. Copy README.md to that folder
echo 4. Zip the folder for distribution
echo.
pause
