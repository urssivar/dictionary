#!/usr/bin/env python3
"""Build all dictionary export formats."""

import sys
from to_urssivar import main as export_urssivar
from to_json import main as export_json
from to_csv import main as export_csv


def main():
    exporters = [export_urssivar, export_json, export_csv]

    success_count = 0
    for exporter_fn in exporters:
        try:
            exporter_fn()
            success_count += 1
        except Exception as e:
            print(f"❌ {e}\n")

    print(f"\n{'✔️' if success_count == len(exporters) else '❌'} {success_count}/{len(exporters)} exports")

    if success_count < len(exporters):
        sys.exit(1)


if __name__ == '__main__':
    main()
