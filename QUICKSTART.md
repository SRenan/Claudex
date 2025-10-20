# Quick Start Guide

Get started with the AOE2 Record APM Analyzer in just a few minutes!

## Installation

### Option 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Claudex

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Install as a Package

```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

After package installation, you can use the `aoe2-apm` command from anywhere:

```bash
aoe2-apm game.aoe2record
```

## Basic Usage

### 1. Analyze a Single Game

```bash
python apm_cli.py /path/to/your/game.aoe2record
```

Output:
```
======================================================================
APM Analysis for: game.aoe2record
======================================================================

Player               Civ             Actions    APM        Winner
----------------------------------------------------------------------
TheViper             Aztecs          8543       142.38     ✓
Hera                 Mayans          8234       137.23

Game Duration: 60.00 minutes
======================================================================
```

### 2. Get JSON Output

```bash
python apm_cli.py game.aoe2record --format json
```

### 3. Analyze Multiple Games

```bash
python apm_cli.py /path/to/records/folder --batch
```

## Where to Find Your Record Files

Age of Empires 2: Definitive Edition saves recorded games in:

**Windows:**
```
C:\Users\<YourUsername>\Games\Age of Empires 2 DE\<SteamID>\savegame\
```

**Linux (Steam Proton):**
```
~/.steam/steam/steamapps/compatdata/813780/pfx/drive_c/users/steamuser/Games/Age of Empires 2 DE/<SteamID>/savegame/
```

**Mac:**
```
~/Library/Application Support/Age of Empires 2 DE/<SteamID>/savegame/
```

## Common Use Cases

### Analyze Your Latest Game

```bash
# On Windows (PowerShell)
python apm_cli.py "$env:USERPROFILE\Games\Age of Empires 2 DE\*\savegame\" --batch

# On Linux
python apm_cli.py ~/.steam/steam/steamapps/compatdata/813780/pfx/drive_c/users/steamuser/Games/Age\ of\ Empires\ 2\ DE/*/savegame/ --batch
```

### Export to JSON for Analysis

```bash
python apm_cli.py game.aoe2record --format json --output results.json
```

Then you can open `results.json` in any text editor or use it in other tools.

### Batch Process and Save Results

```bash
python apm_cli.py /path/to/records/ --batch --format json --output all_games.json
```

## Using in Python Scripts

```python
from apm_analyzer import analyze_apm

# Simple usage
results = analyze_apm('game.aoe2record')

# Access the data
for player in results['players']:
    print(f"{player['name']}: {player['apm']} APM")
```

See `examples.py` for more advanced usage patterns.

## Troubleshooting

### "Module 'mgz' not found"

Install the required dependency:
```bash
pip install mgz
```

### "File not found" Error

Make sure you're using the correct path to your `.aoe2record` file. Use quotes if the path contains spaces:
```bash
python apm_cli.py "path/with spaces/game.aoe2record"
```

### "Error parsing file"

- Ensure the file is a valid `.aoe2record` file from Age of Empires 2: Definitive Edition
- The file might be corrupted or from an unsupported version
- Try with a different record file

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [examples.py](examples.py) for programmatic usage examples
- Report issues or contribute at the GitHub repository

## Tips

1. **Find High APM Games**: Use batch processing to analyze all your games and find your best performances
2. **Track Progress**: Export results to JSON and track your APM over time
3. **Compare with Friends**: Analyze multiplayer games to see how you stack up
4. **Optimize Practice**: Identify which civilizations or strategies lead to higher APM

Happy analyzing!
