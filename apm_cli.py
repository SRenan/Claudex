#!/usr/bin/env python3
"""
Command-line interface for AOE2 Record APM Analyzer
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List

from apm_analyzer import APMAnalyzer, analyze_apm


def find_record_files(directory: str) -> List[str]:
    """
    Find all .aoe2record files in a directory.

    Args:
        directory: Directory path to search

    Returns:
        List of .aoe2record file paths
    """
    record_files = []
    path = Path(directory)

    if path.is_file() and path.suffix == '.aoe2record':
        return [str(path)]

    for file_path in path.rglob('*.aoe2record'):
        record_files.append(str(file_path))

    return sorted(record_files)


def process_single_file(file_path: str, output_format: str = 'text', output_file: str = None):
    """
    Process a single .aoe2record file.

    Args:
        file_path: Path to the record file
        output_format: Output format ('text' or 'json')
        output_file: Optional output file path
    """
    analyzer = APMAnalyzer(file_path)

    if not analyzer.parse():
        print(f"Failed to parse: {file_path}", file=sys.stderr)
        return False

    results = analyzer.get_results()

    if output_format == 'json':
        output = json.dumps(results, indent=2)
        if output_file:
            with open(output_file, 'w') as f:
                f.write(output)
            print(f"Results written to: {output_file}")
        else:
            print(output)
    else:
        analyzer.print_results()

    return True


def process_batch(files: List[str], output_format: str = 'text', output_file: str = None):
    """
    Process multiple .aoe2record files.

    Args:
        files: List of file paths
        output_format: Output format ('text' or 'json')
        output_file: Optional output file path
    """
    all_results = []
    successful = 0
    failed = 0

    for file_path in files:
        print(f"Processing: {file_path}")
        analyzer = APMAnalyzer(file_path)

        if analyzer.parse():
            results = analyzer.get_results()
            all_results.append(results)

            if output_format == 'text':
                analyzer.print_results()

            successful += 1
        else:
            print(f"Failed to parse: {file_path}", file=sys.stderr)
            failed += 1

    print(f"\nProcessed {successful + failed} files: {successful} successful, {failed} failed")

    if output_format == 'json':
        output = json.dumps(all_results, indent=2)
        if output_file:
            with open(output_file, 'w') as f:
                f.write(output)
            print(f"Results written to: {output_file}")
        else:
            print(output)


def main():
    """Main CLI entry point."""
    # If no arguments provided, launch GUI
    if len(sys.argv) == 1:
        try:
            from apm_gui import launch_gui
            launch_gui()
            return
        except ImportError:
            print("GUI dependencies not available. Please provide command-line arguments.", file=sys.stderr)
            print("Run with --help for usage information.", file=sys.stderr)
            sys.exit(1)

    parser = argparse.ArgumentParser(
        description='Extract player APM (Actions Per Minute) from AOE2 record files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with GUI (no arguments)
  aoe2-apm.exe

  # Analyze a single record file
  aoe2-apm.exe game.aoe2record

  # Analyze with JSON output
  aoe2-apm.exe game.aoe2record --format json

  # Analyze all files in a directory
  aoe2-apm.exe /path/to/records/ --batch

  # Save results to a file
  aoe2-apm.exe game.aoe2record --format json --output results.json

  # Batch process and save to JSON
  aoe2-apm.exe /path/to/records/ --batch --format json --output all_results.json
        """
    )

    parser.add_argument(
        'input',
        help='Path to .aoe2record file or directory containing record files'
    )

    parser.add_argument(
        '-b', '--batch',
        action='store_true',
        help='Process all .aoe2record files in the specified directory'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='AOE2 APM Analyzer v1.0.0'
    )

    args = parser.parse_args()

    # Validate input path
    if not os.path.exists(args.input):
        print(f"Error: Path not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.batch:
            # Batch processing
            files = find_record_files(args.input)
            if not files:
                print(f"No .aoe2record files found in: {args.input}", file=sys.stderr)
                sys.exit(1)

            print(f"Found {len(files)} .aoe2record file(s)\n")
            process_batch(files, args.format, args.output)

        else:
            # Single file processing
            if os.path.isdir(args.input):
                print(f"Error: {args.input} is a directory. Use --batch to process directories.",
                      file=sys.stderr)
                sys.exit(1)

            if not args.input.endswith('.aoe2record'):
                print(f"Error: File must have .aoe2record extension", file=sys.stderr)
                sys.exit(1)

            success = process_single_file(args.input, args.format, args.output)
            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
