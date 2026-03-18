#!/usr/bin/env python3
import sys
from pathlib import Path
from utils.paths import ROOT


def parse_output_path(default_filename):
    if len(sys.argv) < 2:
        return ROOT / 'export' / default_filename
    return Path(sys.argv[1])


def print_export_stats(total_entries, skipped_entries, output_path, entries_by_letter=None):
    skipped = f", {skipped_entries} skipped" if skipped_entries else ""
    print(f"\n✔️ {total_entries} entries{skipped} → {output_path}")

    if entries_by_letter:
        for letter, entries in entries_by_letter.items():
            print(f"  {letter}: {len(entries)}")


def map_tags(tags, tag_map):
    if not tags:
        return []
    return [{'en': tag_map[t]['en'], 'ru': tag_map[t]['ru']} for t in tags if t in tag_map]
