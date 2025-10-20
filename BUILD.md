# Building Standalone Executable

This guide explains how to build a standalone Windows executable (`.exe`) that requires **no Python installation** to run.

## Why Build an Executable?

The standalone executable:
- ✅ Works on any Windows PC without Python installed
- ✅ No need to manage dependencies or pip
- ✅ Single file - easy to distribute
- ✅ Just download and run
- ✅ Perfect for end users who aren't developers

## Quick Start

### On Windows

1. **Install Python** (if you don't have it):
   - Download from [python.org](https://www.python.org/downloads/)
   - Python 3.7 or higher required

2. **Run the build script**:
   ```cmd
   build.bat
   ```

3. **Find your executable**:
   ```
   dist\aoe2-apm.exe
   ```

That's it! The `.exe` file is ready to distribute.

### On Linux/Mac (Cross-compilation)

```bash
chmod +x build.sh
./build.sh
```

The resulting `dist/aoe2-apm.exe` will run on Windows.

## Manual Build Process

If you prefer to build manually:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `mgz` - AOE2 record parser
- `pyinstaller` - Executable builder

### Step 2: Build with PyInstaller

```bash
pyinstaller aoe2-apm.spec
```

### Step 3: Find Your Executable

```
dist/aoe2-apm.exe  (Windows executable, ~50-150 MB)
```

## What Gets Included

The executable bundles:
- Python 3.x runtime (~15 MB)
- Python standard library (~30 MB)
- mgz library and dependencies (~15 MB)
- Your application code (~1 MB)

**Total size**: Approximately 50-150 MB (varies based on Python version)

## Using the Executable

Once built, the executable is **completely standalone**:

```cmd
# No Python needed!
aoe2-apm.exe game.aoe2record

# All CLI features work
aoe2-apm.exe game.aoe2record --format json
aoe2-apm.exe C:\Records\ --batch
```

## Distribution

To share with others:

1. **Upload `dist/aoe2-apm.exe`** to your preferred platform:
   - GitHub Releases
   - Google Drive
   - Dropbox
   - Your website

2. **Users download and run** - no installation required

3. **Optional**: Create a ZIP file with:
   ```
   aoe2-apm/
   ├── aoe2-apm.exe
   ├── README.md
   └── QUICKSTART.md
   ```

## Advanced Configuration

### Customizing the Build

Edit `aoe2-apm.spec` to customize:

#### Add an Icon
```python
exe = EXE(
    # ... other settings ...
    icon='path/to/icon.ico',
)
```

#### Exclude More Modules (reduce size)
```python
excludes=[
    'tkinter',
    'matplotlib',
    # Add more here
],
```

#### Enable UPX Compression
UPX can reduce file size by 30-50%:

1. Download UPX from [upx.github.io](https://upx.github.io/)
2. Add to PATH
3. Build again (UPX runs automatically if available)

### One-File vs One-Folder

**Current config**: One-file (single .exe)
- Pros: Easy to distribute
- Cons: Slower startup (extracts to temp folder)

**Alternative**: One-folder (exe + DLLs in folder)
```python
exe = EXE(
    pyz,
    a.scripts,
    # Comment out these lines:
    # a.binaries,
    # a.zipfiles,
    # a.datas,
    # ...
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='aoe2-apm',
)
```

Result: `dist/aoe2-apm/` folder with multiple files
- Pros: Faster startup
- Cons: Must distribute entire folder

## Troubleshooting

### "PyInstaller not found"

```bash
pip install pyinstaller
```

### Build fails with "module not found"

Add the missing module to `hiddenimports` in `aoe2-apm.spec`:

```python
hiddenimports=[
    'mgz',
    'your_missing_module',
],
```

### Executable is too large

1. **Enable UPX compression** (can reduce 30-50%)
2. **Exclude unused modules** in the spec file
3. **Use Python 3.11+** (slightly smaller)

Typical sizes:
- Without UPX: ~100-150 MB
- With UPX: ~50-70 MB

### Antivirus False Positives

Some antivirus software flags PyInstaller executables as suspicious because:
- They self-extract at runtime
- The packing pattern is used by some malware

**Solutions**:
- Submit to antivirus vendors as false positive
- Code-sign your executable (requires certificate, ~$100/year)
- Use PyOxidizer instead of PyInstaller (less common packing pattern)

### Slow Startup (3-5 seconds)

This is normal for PyInstaller one-file executables:
1. Extracts Python to temp folder (~2 sec)
2. Loads interpreter (~1 sec)
3. Imports modules (~1 sec)

**To speed up**:
- Use one-folder mode (no extraction needed)
- Or rewrite in Go/Rust (instant startup)

## Build Artifacts

After building, you'll have:

```
build/          # Temporary build files (can delete)
dist/           # Your executable is here!
  └── aoe2-apm.exe
__pycache__/    # Python cache (can delete)
```

Clean up build artifacts:
```bash
# Windows
rmdir /s /q build dist __pycache__

# Linux/Mac
rm -rf build dist __pycache__
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Build Executable

on: [push]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pyinstaller aoe2-apm.spec
      - uses: actions/upload-artifact@v2
        with:
          name: aoe2-apm-windows
          path: dist/aoe2-apm.exe
```

This automatically builds the executable on every commit.

## Comparison: Executable vs Python

| Aspect | Python Script | Standalone .exe |
|--------|--------------|-----------------|
| **User needs Python** | Yes | No |
| **File size** | ~10 KB | ~50-150 MB |
| **Startup time** | Instant | 2-5 seconds |
| **Distribution** | Complex | Simple |
| **Updates** | Edit file | Rebuild exe |
| **Maintenance** | Easy | Easy |

## Next Steps

Once you have a working executable:

1. **Test thoroughly** on different Windows versions
2. **Create GitHub Release** with the .exe
3. **Write user documentation** assuming no Python knowledge
4. **Consider code signing** for professional distribution

## Need Help?

- Check the [main README](README.md)
- Review the [PyInstaller docs](https://pyinstaller.org/)
- Open an issue on GitHub

Happy building!
