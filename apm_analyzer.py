"""
AOE2 Record APM Analyzer
Extracts and calculates Actions Per Minute (APM) from .aoe2record files.
"""

from mgz.summary import Summary
from mgz import fast
from collections import defaultdict
from typing import Dict, List, Optional, Tuple
import os


class APMAnalyzer:
    """Analyzes .aoe2record files to extract player APM statistics."""

    def __init__(self, record_file_path: str):
        """
        Initialize the APM analyzer with a record file.

        Args:
            record_file_path: Path to the .aoe2record file

        Raises:
            FileNotFoundError: If the record file doesn't exist
            ValueError: If the file is not a valid .aoe2record file
        """
        if not os.path.exists(record_file_path):
            raise FileNotFoundError(f"Record file not found: {record_file_path}")

        if not record_file_path.endswith('.aoe2record'):
            raise ValueError(f"File must be a .aoe2record file: {record_file_path}")

        self.record_file_path = record_file_path
        self.summary = None
        self.players_info = {}
        self.apm_data = {}

    def parse(self) -> bool:
        """
        Parse the record file and extract game data.

        Returns:
            True if parsing was successful, False otherwise
        """
        try:
            with open(self.record_file_path, 'rb') as f:
                self.summary = Summary(f)
                self._extract_player_info()
                self._calculate_apm()
            return True
        except Exception as e:
            print(f"Error parsing file: {e}")
            return False

    def _extract_player_info(self):
        """Extract basic player information from the summary."""
        if not self.summary:
            return

        # Extract player information
        for player in self.summary.get_players():
            player_number = player.get('number')
            if player_number is not None:
                self.players_info[player_number] = {
                    'name': player.get('name', 'Unknown'),
                    'civilization': player.get('civilization', 'Unknown'),
                    'color_id': player.get('color_id'),
                    'winner': player.get('winner', False)
                }

    def _calculate_apm(self):
        """Calculate APM for each player based on their actions."""
        if not self.summary:
            return

        # Get game duration in milliseconds
        duration_ms = self.summary.get_duration()
        if not duration_ms or duration_ms == 0:
            print("Warning: Could not determine game duration")
            return

        # Convert to minutes
        duration_minutes = duration_ms / 1000 / 60

        # Count actions per player
        action_counts = defaultdict(int)

        # Parse actions from the file
        try:
            with open(self.record_file_path, 'rb') as f:
                parser = fast.parse(f)

                # Iterate through all operations/actions
                for operation in parser.get('action', []):
                    player_number = operation.get('player_number')
                    if player_number is not None:
                        action_counts[player_number] += 1
        except Exception as e:
            print(f"Warning: Could not parse actions: {e}")
            # Fallback: try to get action counts from summary
            try:
                for player in self.summary.get_players():
                    player_number = player.get('number')
                    if player_number is not None:
                        # Some versions provide action count directly
                        actions = player.get('action_count', 0)
                        if actions > 0:
                            action_counts[player_number] = actions
            except:
                pass

        # Calculate APM for each player
        for player_number, action_count in action_counts.items():
            apm = action_count / duration_minutes if duration_minutes > 0 else 0

            self.apm_data[player_number] = {
                'total_actions': action_count,
                'apm': round(apm, 2),
                'duration_minutes': round(duration_minutes, 2)
            }

    def get_results(self) -> Dict:
        """
        Get the complete APM analysis results.

        Returns:
            Dictionary containing player info and APM statistics
        """
        results = {
            'file': os.path.basename(self.record_file_path),
            'players': []
        }

        for player_number, player_info in self.players_info.items():
            apm_info = self.apm_data.get(player_number, {})

            player_result = {
                'number': player_number,
                'name': player_info['name'],
                'civilization': player_info['civilization'],
                'winner': player_info['winner'],
                'total_actions': apm_info.get('total_actions', 0),
                'apm': apm_info.get('apm', 0),
                'duration_minutes': apm_info.get('duration_minutes', 0)
            }

            results['players'].append(player_result)

        # Sort players by player number
        results['players'].sort(key=lambda x: x['number'])

        return results

    def print_results(self):
        """Print APM results in a human-readable format."""
        results = self.get_results()

        print(f"\n{'='*70}")
        print(f"APM Analysis for: {results['file']}")
        print(f"{'='*70}\n")

        if not results['players']:
            print("No player data available.")
            return

        # Print header
        print(f"{'Player':<20} {'Civ':<15} {'Actions':<10} {'APM':<10} {'Winner':<8}")
        print(f"{'-'*70}")

        # Print each player
        for player in results['players']:
            winner_mark = '✓' if player['winner'] else ''
            print(f"{player['name']:<20} "
                  f"{player['civilization']:<15} "
                  f"{player['total_actions']:<10} "
                  f"{player['apm']:<10.2f} "
                  f"{winner_mark:<8}")

        # Print game duration
        if results['players']:
            duration = results['players'][0]['duration_minutes']
            print(f"\nGame Duration: {duration:.2f} minutes")

        print(f"{'='*70}\n")


def analyze_apm(record_file_path: str, print_output: bool = True) -> Optional[Dict]:
    """
    Convenience function to analyze APM from a record file.

    Args:
        record_file_path: Path to the .aoe2record file
        print_output: Whether to print the results (default: True)

    Returns:
        Dictionary with APM results, or None if parsing failed
    """
    analyzer = APMAnalyzer(record_file_path)

    if analyzer.parse():
        results = analyzer.get_results()
        if print_output:
            analyzer.print_results()
        return results
    else:
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python apm_analyzer.py <path_to_aoe2record_file>")
        sys.exit(1)

    record_file = sys.argv[1]
    analyze_apm(record_file)
