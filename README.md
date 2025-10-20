# AOE2 Record APM Analyzer

A Python tool for extracting and analyzing player APM (Actions Per Minute) from Age of Empires 2 recorded game files (`.aoe2record`).

## Features

- Parse `.aoe2record` files from Age of Empires 2: Definitive Edition
- Extract player APM statistics for all players in a game
- Display player information including name, civilization, and winner status
- Support for single file and batch processing
- Output in human-readable text or JSON format
- Export results to file
- **Standalone Windows executable available** (no Python installation required!)

## Getting Started

### Option 1: Standalone Executable (Recommended for Windows Users)

**No Python installation required!**

1. Download the latest `aoe2-apm.exe` from the [Releases](../../releases) page
2. Run it from the command line:
   ```cmd
   aoe2-apm.exe game.aoe2record
   ```

That's it! See [BUILD.md](BUILD.md) for how to build the executable yourself.

### Option 2: Python Script (For Developers)

## Requirements

- Python 3.7 or higher
- `mgz` library (Age of Empires II recorded game parser)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Claudex
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Basic Usage

Analyze a single record file:
```bash
python apm_cli.py game.aoe2record
```

#### JSON Output

Get results in JSON format:
```bash
python apm_cli.py game.aoe2record --format json
```

#### Save to File

Save results to a file:
```bash
python apm_cli.py game.aoe2record --format json --output results.json
```

#### Batch Processing

Process all `.aoe2record` files in a directory:
```bash
python apm_cli.py /path/to/records/ --batch
```

Batch process and save to JSON:
```bash
python apm_cli.py /path/to/records/ --batch --format json --output all_results.json
```

### Python API

You can also use the analyzer directly in your Python code:

```python
from apm_analyzer import APMAnalyzer, analyze_apm

# Simple usage with automatic output
results = analyze_apm('game.aoe2record')

# Or use the class for more control
analyzer = APMAnalyzer('game.aoe2record')
if analyzer.parse():
    results = analyzer.get_results()
    analyzer.print_results()

    # Access individual player data
    for player in results['players']:
        print(f"{player['name']}: {player['apm']} APM")
```

## Output Format

### Text Output

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

### JSON Output

```json
{
  "file": "game.aoe2record",
  "players": [
    {
      "number": 1,
      "name": "TheViper",
      "civilization": "Aztecs",
      "winner": true,
      "total_actions": 8543,
      "apm": 142.38,
      "duration_minutes": 60.0
    },
    {
      "number": 2,
      "name": "Hera",
      "civilization": "Mayans",
      "winner": false,
      "total_actions": 8234,
      "apm": 137.23,
      "duration_minutes": 60.0
    }
  ]
}
```

## CLI Options

```
usage: apm_cli.py [-h] [-b] [-f {text,json}] [-o OUTPUT] [-v] input

positional arguments:
  input                 Path to .aoe2record file or directory

optional arguments:
  -h, --help            Show help message and exit
  -b, --batch           Process all .aoe2record files in directory
  -f, --format {text,json}
                        Output format (default: text)
  -o, --output OUTPUT   Output file path (default: stdout)
  -v, --version         Show version and exit
```

## How It Works

1. **File Parsing**: The tool uses the `mgz` library to parse `.aoe2record` files, which contain the complete game state and all player actions.

2. **Action Extraction**: It extracts all player actions from the recorded game data.

3. **APM Calculation**: APM is calculated using the formula:
   ```
   APM = Total Actions / Game Duration (in minutes)
   ```

4. **Player Information**: Additional player information (name, civilization, winner status) is extracted from the game summary.

## Understanding APM

- **APM (Actions Per Minute)**: The total number of actions a player performs divided by the game duration
- Professional players typically have APM ranging from 80-150+
- Higher APM generally indicates faster gameplay, but effective actions matter more than raw numbers

## Troubleshooting

### Common Issues

**"Error parsing file"**
- Ensure the file is a valid `.aoe2record` file from Age of Empires 2: Definitive Edition
- Check that the file is not corrupted

**"No player data available"**
- The record file may be from a very old version or corrupted
- Try with a different record file

**"Could not determine game duration"**
- This can happen with incomplete or corrupted recordings
- The APM calculation will be skipped for such files

## Examples

Check the `examples.py` file for more usage examples.

## Dependencies

- [mgz](https://github.com/happyleavesaoc/aoc-mgz) - Age of Empires II recorded game parser

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

- Thanks to the creators of the `mgz` library for providing the AOE2 record file parser
- Age of Empires 2 community for their support and feedback
