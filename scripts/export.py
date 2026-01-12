#!/usr/bin/env python3
"""Build all dictionary export formats."""

import subprocess
import sys
from pathlib import Path


def run_script(script_path):
    """Run a Python script and handle errors."""
    script_name = script_path.name
    print(f"Running {script_name}...")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        print(f"✓ {script_name} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {script_name} failed with error:")
        print(e.stderr)
        return False


def main():
    """Run all export scripts."""
    scripts_dir = Path(__file__).parent

    export_scripts = [
        scripts_dir / 'to_json_web.py',
        scripts_dir / 'to_json_archive.py',
        scripts_dir / 'to_csv.py',
    ]

    print("Building dictionary exports...\n")

    success_count = 0
    for script in export_scripts:
        if not script.exists():
            print(f"Warning: {script.name} not found, skipping...")
            continue

        if run_script(script):
            success_count += 1
        print()  # Blank line between scripts

    print(f"Export complete: {success_count}/{len(export_scripts)} scripts succeeded")

    if success_count < len(export_scripts):
        sys.exit(1)


if __name__ == '__main__':
    main()
