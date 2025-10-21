# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for AOE2 APM Analyzer
This creates a standalone Windows executable with no external dependencies.
Supports both GUI (double-click) and CLI (command-line) modes.

Usage:
    pyinstaller aoe2-apm.spec
"""

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Collect all data files from mgz package (includes JSON reference data)
mgz_datas = collect_data_files('mgz')

a = Analysis(
    ['apm_cli.py', 'apm_gui.py'],  # Include both CLI and GUI
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('LICENSE', '.'),
    ] + mgz_datas,  # Add mgz data files
    hiddenimports=[
        'mgz',
        'mgz.summary',
        'mgz.fast',
        'mgz.header',
        'mgz.body',
        'mgz.model',
        'mgz.reference',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unused modules to reduce size
        # Note: tkinter is now INCLUDED for GUI support
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='aoe2-apm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress with UPX if available
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console application (for CLI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an icon file here if you have one
)
