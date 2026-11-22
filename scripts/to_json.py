#!/usr/bin/env python3
"""Convert Kaitag YAML entries to complete JSON archive (unprocessed format for research/tools)."""

import json
from utils.paths import ROOT
from utils.meta import load_alphabet
from utils.entries import load_entries
from utils.text import sorting_key


def main():
    output_path = ROOT / 'export' / 'dictionary.json'

    entries_by_letter, total_entries, skipped_entries = load_entries()

    entries = []
    for letter in load_alphabet()['alphabet']:
        entries.extend(entries_by_letter.get(letter, []))
    entries.sort(key=sorting_key)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    skipped = f", {skipped_entries} skipped" if skipped_entries else ""
    print(f"\n✔️ {total_entries} entries{skipped} → {output_path}")


if __name__ == '__main__':
    main()
