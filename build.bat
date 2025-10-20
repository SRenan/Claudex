@echo off
REM Build script for AOE2 APM Analyzer Windows executable
REM This creates a standalone .exe with no dependencies

echo ========================================
echo AOE2 APM Analyzer - Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    exit /b 1
)

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo.
echo [2/4] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo [3/4] Building executable with PyInstaller...
pyinstaller aoe2-apm.spec
if errorlevel 1 (
    echo ERROR: Build failed
    exit /b 1
)

echo.
echo [4/4] Build complete!
echo.
echo ========================================
echo Executable created: dist\aoe2-apm.exe
echo ========================================
echo.
echo File size:
dir dist\aoe2-apm.exe | find "aoe2-apm.exe"
echo.
echo You can now distribute dist\aoe2-apm.exe
echo It requires no Python installation to run.
echo.

pause
