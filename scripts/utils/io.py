#!/usr/bin/env python3
"""Export pipeline utilities: output path, validation, stats, tag mapping."""

import sys
from pathlib import Path


def parse_output_path(default_filename):
    """Return output path from CLI arg or default export/ directory."""
    if len(sys.argv) < 2:
        return Path(__file__).parent.parent.parent / 'export' / default_filename
    return Path(sys.argv[1])


def validate_entry(yaml_data):
    """Return True if entry has required fields: id, headword, definitions."""
    return ('id' in yaml_data and
            'headword' in yaml_data and
            'definitions' in yaml_data)


def print_export_stats(total_entries, skipped_entries, output_path, entries_by_letter=None):
    """Print standardized export statistics."""
    print(f"\nConversion complete!")
    print(f"Total entries: {total_entries}")
    print(f"Skipped entries: {skipped_entries}")
    print(f"Output written to: {output_path}")

    if entries_by_letter:
        print(f"\nEntries per letter:")
        for letter, entries in entries_by_letter.items():
            print(f"  {letter}: {len(entries)}")


def map_tags(tags, tag_map):
    """Map tag list to bilingual [{en, ru}] objects, filtering unknown tags."""
    if not tags:
        return []
    return [{'en': tag_map[t]['en'], 'ru': tag_map[t]['ru']} for t in tags if t in tag_map]
