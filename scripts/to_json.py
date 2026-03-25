#!/usr/bin/env python3
"""Convert Kaitag YAML lexicon to complete JSON archive (unprocessed format for research/tools)."""

import json
from utils import ROOT, load_alphabet, load_lexicon_entries


def main():
    output_path = ROOT / 'export' / 'dictionary.json'

    alphabet, _, _, sorting_key = load_alphabet()
    entries_by_letter, total_entries, skipped_entries = load_lexicon_entries(alphabet)

    entries = []
    for letter in alphabet:
        for e in entries_by_letter.get(letter, []):
            e['id'] = e.pop('_id')
            entries.append(e)
    entries.sort(key=sorting_key)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    skipped = f", {skipped_entries} skipped" if skipped_entries else ""
    print(f"\n✔️ {total_entries} entries{skipped} → {output_path}")


if __name__ == '__main__':
    main()
