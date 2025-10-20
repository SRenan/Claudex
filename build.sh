#!/bin/bash
# Build script for AOE2 APM Analyzer Windows executable
# This creates a standalone .exe with no dependencies
# Can be run on Linux/Mac to cross-compile for Windows

set -e

echo "========================================"
echo "AOE2 APM Analyzer - Build Script"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[1/4] Installing dependencies..."
pip install -r requirements.txt

echo
echo "[2/4] Cleaning previous builds..."
rm -rf build dist __pycache__

echo
echo "[3/4] Building executable with PyInstaller..."
pyinstaller aoe2-apm.spec

echo
echo "[4/4] Build complete!"
echo
echo "========================================"
echo "Executable created: dist/aoe2-apm.exe"
echo "========================================"
echo
echo "File size:"
ls -lh dist/aoe2-apm.exe | awk '{print $5, $9}'
echo
echo "You can now distribute dist/aoe2-apm.exe"
echo "It requires no Python installation to run."
echo
