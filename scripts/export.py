#!/usr/bin/env python3
"""Build all dictionary export formats."""

import sys
from validate import main as validate_main
from to_json_web import main as export_web
from to_json_archive import main as export_archive
from to_csv import main as export_csv


def main():
    print("🔍 Validating...")
    try:
        validate_main()
    except SystemExit as e:
        if e.code != 0:
            print("⛔ Export aborted.")
            sys.exit(1)

    print("\n📦 Exporting...\n")

    exporters = [export_web, export_archive, export_csv]

    success_count = 0
    for exporter_fn in exporters:
        name = exporter_fn.__name__
        print(f"  {name}...")
        try:
            exporter_fn()
            print(f"✔️ done\n")
            success_count += 1
        except Exception as e:
            print(f"❌ {e}\n")

    print(f"{'✔️' if success_count == len(exporters) else '❌'} {success_count}/{len(exporters)} succeeded")

    if success_count < len(exporters):
        sys.exit(1)


if __name__ == '__main__':
    main()
