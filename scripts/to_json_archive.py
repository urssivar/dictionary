#!/usr/bin/env python3
"""Convert Kaitag YAML lexicon to complete JSON archive (unprocessed format for research/tools)."""

import json
import yaml
import sys
from pathlib import Path
from utils import (
    load_alphabet,
    create_tokenizer,
    parse_output_path,
    validate_entry,
    print_export_stats,
    load_lexicon_entries
)


def main():
    # Use new utility for output path
    output_file = parse_output_path('dictionary-archive.json')

    # Load data files
    alphabet, alphabet_tokens, _ = load_alphabet()
    sorting_key = create_tokenizer(alphabet, alphabet_tokens)

    # Load all entries using new utility
    entries_by_letter, total_entries, skipped_entries = load_lexicon_entries(
        alphabet,
        validate_fn=validate_entry
    )

    # Sort entries per letter (entries already loaded, just need sorting)
    for letter in entries_by_letter:
        entries_by_letter[letter].sort(key=sorting_key)

    # Write output
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(entries_by_letter, f, ensure_ascii=False, indent=2)

    # Print stats using new utility
    print_export_stats(total_entries, skipped_entries, output_path, entries_by_letter)


if __name__ == '__main__':
    main()
