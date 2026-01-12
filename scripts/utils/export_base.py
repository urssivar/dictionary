#!/usr/bin/env python3
"""Common export utilities for dictionary scripts."""

import sys
import yaml
from pathlib import Path


def parse_output_path(default_filename):
    """Parse output file path from command line or use default in export/."""
    if len(sys.argv) < 2:
        return Path(__file__).parent.parent.parent / 'export' / default_filename
    return Path(sys.argv[1])


def validate_entry(yaml_data):
    """Validate that YAML entry has required fields: id, headword, definitions."""
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


def load_lexicon_entries(alphabet, validate_fn=None):
    """
    Load all lexicon entries from YAML files organized by letter.

    Args:
        alphabet: List of letters to process
        validate_fn: Optional validation function for entries

    Returns:
        tuple: (entries_by_letter dict, total_entries, skipped_entries)
    """
    lexicon_dir = Path(__file__).parent.parent.parent / 'lexicon'
    entries_by_letter = {}
    total_entries = 0
    skipped_entries = 0

    for letter in alphabet:
        letter_dir = lexicon_dir / letter
        if not letter_dir.exists():
            print(f"Warning: Directory not found for letter '{letter}'")
            continue

        entries_by_letter[letter] = []

        for yaml_file in sorted(letter_dir.glob('*.yaml')):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)

                # Validate if function provided
                if validate_fn and not validate_fn(yaml_data):
                    skipped_entries += 1
                    print(f"Warning: Skipped {yaml_file.name} (missing required fields)")
                    continue

                entries_by_letter[letter].append(yaml_data)
                total_entries += 1

            except Exception as e:
                skipped_entries += 1
                print(f"Error processing {yaml_file.name}: {e}")

    return entries_by_letter, total_entries, skipped_entries
