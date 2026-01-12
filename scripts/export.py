#!/usr/bin/env python3
"""Build all dictionary export formats."""

import sys
from validate import main as validate_main
from to_json_web import main as export_web
from to_json_archive import main as export_archive
from to_csv import main as export_csv


def main():
    """Run validation, then all export scripts."""

    # Run validation
    print("Validating entries...")
    try:
        validate_main()
    except SystemExit as e:
        if e.code != 0:
            print("Export aborted due to validation errors.\n")
            sys.exit(1)

    print("\nBuilding dictionary exports...\n")

    # Run exporters
    exporters = [
        ("to_json_web.py", export_web),
        ("to_json_archive.py", export_archive),
        ("to_csv.py", export_csv),
    ]

    success_count = 0
    for name, exporter_fn in exporters:
        print(f"Running {name}...")
        try:
            exporter_fn()
            print(f"✓ {name} completed successfully\n")
            success_count += 1
        except Exception as e:
            print(f"✗ {name} failed with error:")
            print(str(e))
            print()

    print(f"Export complete: {success_count}/{len(exporters)} scripts succeeded")

    if success_count < len(exporters):
        sys.exit(1)


if __name__ == '__main__':
    main()
