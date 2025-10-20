"""
Examples of using the AOE2 Record APM Analyzer programmatically
"""

from apm_analyzer import APMAnalyzer, analyze_apm
import json


def example_1_simple_analysis():
    """Example 1: Simple analysis with automatic output"""
    print("Example 1: Simple Analysis")
    print("-" * 50)

    # The simplest way to analyze a file
    results = analyze_apm('game.aoe2record', print_output=True)

    if results:
        print("Analysis completed successfully!")
    else:
        print("Analysis failed!")


def example_2_get_specific_data():
    """Example 2: Extract specific player data"""
    print("\nExample 2: Extract Specific Data")
    print("-" * 50)

    analyzer = APMAnalyzer('game.aoe2record')

    if analyzer.parse():
        results = analyzer.get_results()

        # Get the player with highest APM
        if results['players']:
            top_player = max(results['players'], key=lambda p: p['apm'])
            print(f"Highest APM: {top_player['name']} with {top_player['apm']} APM")

            # Get the winner
            winner = next((p for p in results['players'] if p['winner']), None)
            if winner:
                print(f"Winner: {winner['name']} ({winner['civilization']})")


def example_3_compare_players():
    """Example 3: Compare players and calculate differences"""
    print("\nExample 3: Compare Players")
    print("-" * 50)

    analyzer = APMAnalyzer('game.aoe2record')

    if analyzer.parse():
        results = analyzer.get_results()

        if len(results['players']) >= 2:
            players = results['players']

            print(f"\nPlayer Comparison:")
            for i, player1 in enumerate(players):
                for player2 in players[i + 1:]:
                    apm_diff = abs(player1['apm'] - player2['apm'])
                    action_diff = abs(player1['total_actions'] - player2['total_actions'])

                    print(f"\n{player1['name']} vs {player2['name']}:")
                    print(f"  APM Difference: {apm_diff:.2f}")
                    print(f"  Total Actions Difference: {action_diff}")


def example_4_batch_analysis():
    """Example 4: Analyze multiple files and generate report"""
    print("\nExample 4: Batch Analysis")
    print("-" * 50)

    import os
    from pathlib import Path

    # Find all .aoe2record files in current directory
    record_files = list(Path('.').glob('*.aoe2record'))

    if not record_files:
        print("No .aoe2record files found in current directory")
        return

    all_results = []

    for file_path in record_files:
        print(f"\nAnalyzing: {file_path}")
        analyzer = APMAnalyzer(str(file_path))

        if analyzer.parse():
            results = analyzer.get_results()
            all_results.append(results)

    # Generate summary statistics
    if all_results:
        all_apms = []
        for game in all_results:
            for player in game['players']:
                all_apms.append(player['apm'])

        if all_apms:
            avg_apm = sum(all_apms) / len(all_apms)
            max_apm = max(all_apms)
            min_apm = min(all_apms)

            print(f"\n{'='*50}")
            print(f"Summary Statistics ({len(all_results)} games)")
            print(f"{'='*50}")
            print(f"Average APM: {avg_apm:.2f}")
            print(f"Maximum APM: {max_apm:.2f}")
            print(f"Minimum APM: {min_apm:.2f}")


def example_5_export_to_json():
    """Example 5: Export results to JSON file"""
    print("\nExample 5: Export to JSON")
    print("-" * 50)

    analyzer = APMAnalyzer('game.aoe2record')

    if analyzer.parse():
        results = analyzer.get_results()

        # Save to JSON file
        output_file = 'apm_results.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Results exported to: {output_file}")


def example_6_filter_by_civilization():
    """Example 6: Filter and analyze by civilization"""
    print("\nExample 6: Filter by Civilization")
    print("-" * 50)

    analyzer = APMAnalyzer('game.aoe2record')

    if analyzer.parse():
        results = analyzer.get_results()

        # Group players by civilization
        civ_stats = {}

        for player in results['players']:
            civ = player['civilization']
            if civ not in civ_stats:
                civ_stats[civ] = []
            civ_stats[civ].append(player['apm'])

        # Calculate average APM per civilization
        print("Average APM by Civilization:")
        for civ, apms in civ_stats.items():
            avg_apm = sum(apms) / len(apms)
            print(f"  {civ}: {avg_apm:.2f} APM ({len(apms)} player(s))")


def example_7_custom_output():
    """Example 7: Create custom formatted output"""
    print("\nExample 7: Custom Output Format")
    print("-" * 50)

    analyzer = APMAnalyzer('game.aoe2record')

    if analyzer.parse():
        results = analyzer.get_results()

        print(f"\nGame: {results['file']}")
        print("\nLeaderboard:")

        # Sort players by APM in descending order
        sorted_players = sorted(results['players'], key=lambda p: p['apm'], reverse=True)

        for rank, player in enumerate(sorted_players, 1):
            winner_badge = " 👑" if player['winner'] else ""
            print(f"{rank}. {player['name']} ({player['civilization']}){winner_badge}")
            print(f"   APM: {player['apm']:.2f} | Actions: {player['total_actions']:,}")


def example_8_error_handling():
    """Example 8: Proper error handling"""
    print("\nExample 8: Error Handling")
    print("-" * 50)

    file_paths = ['game.aoe2record', 'nonexistent.aoe2record', 'invalid.txt']

    for file_path in file_paths:
        print(f"\nTrying to analyze: {file_path}")

        try:
            analyzer = APMAnalyzer(file_path)

            if analyzer.parse():
                results = analyzer.get_results()
                print(f"  ✓ Successfully parsed: {len(results['players'])} players found")
            else:
                print(f"  ✗ Failed to parse the file")

        except FileNotFoundError:
            print(f"  ✗ File not found")
        except ValueError as e:
            print(f"  ✗ Invalid file: {e}")
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")


if __name__ == '__main__':
    print("AOE2 Record APM Analyzer - Examples")
    print("=" * 50)

    # Uncomment the example you want to run
    # Note: These examples assume you have .aoe2record files in the current directory

    print("\nTo run these examples, you need .aoe2record files.")
    print("Update the file paths in the examples and uncomment them.\n")

    # example_1_simple_analysis()
    # example_2_get_specific_data()
    # example_3_compare_players()
    # example_4_batch_analysis()
    # example_5_export_to_json()
    # example_6_filter_by_civilization()
    # example_7_custom_output()
    # example_8_error_handling()

    print("\nExamples are ready to use!")
    print("Edit this file to uncomment and run specific examples.")
