"""
GUI interface for AOE2 Record APM Analyzer
Provides a user-friendly graphical interface for analyzing .aoe2record files
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import json
from pathlib import Path
from apm_analyzer import APMAnalyzer


class APMAnalyzerGUI:
    """Graphical user interface for APM analysis."""

    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("AOE2 APM Analyzer")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Set icon if available (optional)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # Variables
        self.current_file = None
        self.current_results = None

        # Create UI
        self.create_widgets()

        # Center window
        self.center_window()

    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="AOE2 Record APM Analyzer",
            font=("Segoe UI", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="Select an Age of Empires 2 recorded game file (.aoe2record) to analyze player APM statistics",
            wraplength=750,
            justify=tk.CENTER
        )
        instructions.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20))

        # Buttons
        select_btn = ttk.Button(
            button_frame,
            text="📁 Select File",
            command=self.select_file,
            width=20
        )
        select_btn.grid(row=0, column=0, padx=5)

        select_folder_btn = ttk.Button(
            button_frame,
            text="📂 Select Folder (Batch)",
            command=self.select_folder,
            width=20
        )
        select_folder_btn.grid(row=0, column=1, padx=5)

        export_btn = ttk.Button(
            button_frame,
            text="💾 Export JSON",
            command=self.export_json,
            width=20
        )
        export_btn.grid(row=0, column=2, padx=5)
        self.export_btn = export_btn
        self.export_btn.state(['disabled'])

        # Results area
        results_label = ttk.Label(main_frame, text="Results:", font=("Segoe UI", 10, "bold"))
        results_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))

        # Scrolled text for results
        self.results_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=90,
            height=20,
            font=("Consolas", 9)
        )
        self.results_text.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(4, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        # Initial message
        self.show_welcome_message()

    def show_welcome_message(self):
        """Display welcome message in results area."""
        welcome = """
╔══════════════════════════════════════════════════════════════════════════╗
║                     Welcome to AOE2 APM Analyzer!                        ║
╚══════════════════════════════════════════════════════════════════════════╝

Get started:
  1. Click "Select File" to analyze a single .aoe2record file
  2. Click "Select Folder" to analyze all .aoe2record files in a directory
  3. View APM statistics for all players in the game
  4. Export results to JSON for further analysis

Where to find your recorded games:
  Windows: C:\\Users\\YourName\\Games\\Age of Empires 2 DE\\<ID>\\savegame\\

The tool will show:
  • Player names and civilizations
  • Total actions performed
  • Actions Per Minute (APM)
  • Game winner
  • Game duration

Ready to analyze your games!
        """
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, welcome)

    def select_file(self):
        """Open file dialog to select a .aoe2record file."""
        filename = filedialog.askopenfilename(
            title="Select AOE2 Record File",
            filetypes=[
                ("AOE2 Record Files", "*.aoe2record"),
                ("All Files", "*.*")
            ],
            initialdir=self.get_default_directory()
        )

        if filename:
            self.analyze_file(filename)

    def select_folder(self):
        """Open folder dialog to batch process .aoe2record files."""
        folder = filedialog.askdirectory(
            title="Select Folder Containing AOE2 Record Files",
            initialdir=self.get_default_directory()
        )

        if folder:
            self.analyze_folder(folder)

    def get_default_directory(self):
        """Get the default directory for AOE2 saved games."""
        # Try to find AOE2 save directory
        user_home = Path.home()
        aoe2_dir = user_home / "Games" / "Age of Empires 2 DE"

        if aoe2_dir.exists():
            return str(aoe2_dir)

        return str(user_home)

    def analyze_file(self, filename):
        """Analyze a single .aoe2record file."""
        self.status_var.set(f"Analyzing: {os.path.basename(filename)}...")
        self.root.update()

        try:
            analyzer = APMAnalyzer(filename)

            if analyzer.parse():
                results = analyzer.get_results()
                self.current_file = filename
                self.current_results = results
                self.display_results(results)
                self.export_btn.state(['!disabled'])
                self.status_var.set(f"✓ Analysis complete: {os.path.basename(filename)}")
            else:
                self.show_error("Failed to parse the record file. The file may be corrupted or invalid.")
                self.status_var.set("✗ Analysis failed")

        except Exception as e:
            self.show_error(f"Error analyzing file:\n{str(e)}")
            self.status_var.set("✗ Error occurred")

    def analyze_folder(self, folder):
        """Analyze all .aoe2record files in a folder."""
        # Find all .aoe2record files
        files = list(Path(folder).glob("*.aoe2record"))

        if not files:
            messagebox.showwarning(
                "No Files Found",
                f"No .aoe2record files found in:\n{folder}"
            )
            return

        self.status_var.set(f"Found {len(files)} file(s). Analyzing...")
        self.root.update()

        all_results = []
        successful = 0
        failed = 0

        for file_path in files:
            try:
                analyzer = APMAnalyzer(str(file_path))
                if analyzer.parse():
                    results = analyzer.get_results()
                    all_results.append(results)
                    successful += 1
                else:
                    failed += 1
            except:
                failed += 1

        self.current_results = all_results
        self.display_batch_results(all_results, successful, failed)
        self.export_btn.state(['!disabled'])
        self.status_var.set(f"✓ Analyzed {successful} files ({failed} failed)")

    def display_results(self, results):
        """Display analysis results for a single file."""
        self.results_text.delete(1.0, tk.END)

        output = f"""
{'='*78}
APM Analysis for: {results['file']}
{'='*78}

"""

        if not results['players']:
            output += "No player data available.\n"
        else:
            # Header
            output += f"{'Player':<25} {'Civilization':<15} {'Actions':<12} {'APM':<10} {'Winner'}\n"
            output += f"{'-'*78}\n"

            # Players
            for player in results['players']:
                winner_mark = '✓' if player['winner'] else ''
                output += f"{player['name']:<25} "
                output += f"{player['civilization']:<15} "
                output += f"{player['total_actions']:<12} "
                output += f"{player['apm']:<10.2f} "
                output += f"{winner_mark}\n"

            # Duration
            if results['players']:
                duration = results['players'][0]['duration_minutes']
                output += f"\nGame Duration: {duration:.2f} minutes\n"

        output += f"\n{'='*78}\n"

        self.results_text.insert(1.0, output)

    def display_batch_results(self, all_results, successful, failed):
        """Display results for batch analysis."""
        self.results_text.delete(1.0, tk.END)

        output = f"""
{'='*78}
Batch Analysis Results
{'='*78}

Processed: {successful + failed} files
Successful: {successful}
Failed: {failed}

"""

        for results in all_results:
            output += f"\n{'─'*78}\n"
            output += f"File: {results['file']}\n"
            output += f"{'─'*78}\n"

            for player in results['players']:
                winner_mark = '👑' if player['winner'] else '  '
                output += f"{winner_mark} {player['name']:<20} ({player['civilization']:<12}) - {player['apm']:.2f} APM\n"

        output += f"\n{'='*78}\n"

        self.results_text.insert(1.0, output)

    def export_json(self):
        """Export current results to JSON file."""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to export. Analyze a file first.")
            return

        filename = filedialog.asksaveasfilename(
            title="Save Results as JSON",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_results, f, indent=2)

                messagebox.showinfo("Success", f"Results exported to:\n{filename}")
                self.status_var.set(f"✓ Exported to: {os.path.basename(filename)}")

            except Exception as e:
                self.show_error(f"Failed to export JSON:\n{str(e)}")

    def show_error(self, message):
        """Show error message dialog."""
        messagebox.showerror("Error", message)


def launch_gui():
    """Launch the GUI application."""
    root = tk.Tk()
    app = APMAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
