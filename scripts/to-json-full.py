#!/usr/bin/env python3
"""Convert Kaitag YAML lexicon to complete JSON for research/tools."""

import json
import yaml
import sys
from pathlib import Path
from utils import (
    load_alphabet,
    get_first_letter,
    create_tokenizer
)


def convert_entry_full(yaml_entry):
    """Convert single YAML entry to JSON with minimal transformation.

    Preserves original structure as much as possible.
    """
    # Validate required fields
    if 'id' not in yaml_entry or 'headword' not in yaml_entry or 'definitions' not in yaml_entry:
        return None

    # Return entry as-is, preserving all fields
    return yaml_entry


def main():
    # Default output to export/dictionary-full.json if not specified
    if len(sys.argv) < 2:
        output_file = Path(__file__).parent.parent / 'export' / 'dictionary-full.json'
    else:
        output_file = sys.argv[1]

    # Load alphabet for sorting
    alphabet, alphabet_tokens, _ = load_alphabet()

    # Create sorting function (based on original headword, no stress marks)
    def make_sorting_key():
        tokenizer = create_tokenizer(alphabet, alphabet_tokens)
        def key(entry):
            return tokenizer(entry)
        return key

    sorting_key = make_sorting_key()

    # Process all letters
    output = {}
    total_entries = 0
    skipped_entries = 0

    lexicon_dir = Path(__file__).parent.parent / 'lexicon'

    for letter in alphabet:
        letter_dir = lexicon_dir / letter
        if not letter_dir.exists():
            print(f"Warning: Directory not found for letter '{letter}'")
            continue

        entries = []

        # Load all YAML files in letter directory
        for yaml_file in sorted(letter_dir.glob('*.yaml')):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)

                converted = convert_entry_full(yaml_data)
                if converted:
                    entries.append(converted)
                    total_entries += 1
                else:
                    skipped_entries += 1
                    print(
                        f"Warning: Skipped {yaml_file.name} (missing required fields)")

            except Exception as e:
                skipped_entries += 1
                print(f"Error processing {yaml_file.name}: {e}")

        # Sort entries
        entries.sort(key=sorting_key)
        output[letter] = entries

    # Write output JSON
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Report statistics
    print(f"\nConversion complete!")
    print(f"Total entries: {total_entries}")
    print(f"Skipped entries: {skipped_entries}")
    print(f"Output written to: {output_path}")

    # Entries per letter
    print(f"\nEntries per letter:")
    for letter in alphabet:
        if letter in output:
            print(f"  {letter}: {len(output[letter])}")


if __name__ == '__main__':
    main()
