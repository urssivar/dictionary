#!/usr/bin/env python3
"""Convert Kaitag YAML lexicon to CSV for linguistic researchers."""

import csv
from utils import ROOT, load_alphabet, load_grammar_tags, mark_stress, simplify_forms, load_lexicon_entries


def get_tags_stacked(tags, tag_map):
    if not tags:
        return ''
    mapped = [{'en': tag_map[t]['en'], 'ru': tag_map[t]['ru']} for t in tags if t in tag_map]
    if not mapped:
        return ''
    return f"{' '.join(t['en'] for t in mapped)}\n{' '.join(t['ru'] for t in mapped)}"


def get_headword_with_ipa(entry, vowels):
    headword = mark_stress(entry, vowels)
    if entry.get('ipa'):
        return f"{headword}\n{entry['ipa']}"
    return headword


def get_definitions(definitions, lang):
    if not definitions:
        return ''
    return '\n'.join(
        str(defn['translation'][lang])
        for defn in definitions
        if 'translation' in defn and lang in defn['translation'] and defn['translation'][lang]
    )


def get_forms(forms, headword):
    if not forms:
        return ''
    return '\n'.join(simplify_forms(forms, headword))


def convert_entry_to_csv(yaml_entry, vowels, tag_map):
    return {
        'letter': '',
        'tags': get_tags_stacked(yaml_entry.get('tags', []), tag_map),
        'headword': get_headword_with_ipa(yaml_entry, vowels),
        'eng': get_definitions(yaml_entry.get('definitions', []), 'en'),
        'rus': get_definitions(yaml_entry.get('definitions', []), 'ru'),
        'forms': get_forms(yaml_entry.get('forms', []), yaml_entry['headword']),
        'variants': '\n'.join(yaml_entry.get('variants') or []),
    }


def main():
    output_path = ROOT / 'export' / 'dictionary.csv'

    alphabet, _, vowels, sorting_key = load_alphabet()
    tag_map = load_grammar_tags()
    entries_by_letter, total_entries, skipped_entries = load_lexicon_entries(alphabet)

    all_entries = []
    for letter in alphabet:
        entries = [
            convert_entry_to_csv(entry, vowels, tag_map)
            for entry in entries_by_letter.get(letter, [])
        ]
        entries.sort(key=lambda e: sorting_key({'headword': e['headword'].split('\n')[0]}))

        all_entries.append({'letter': letter, 'tags': '', 'headword': '', 'eng': '', 'rus': '', 'forms': '', 'variants': ''})
        all_entries.extend(entries)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ['letter', 'tags', 'headword', 'eng', 'rus', 'forms', 'variants']
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_entries)

    skipped = f", {skipped_entries} skipped" if skipped_entries else ""
    print(f"\n✔️ {total_entries} entries{skipped} → {output_path}")


if __name__ == '__main__':
    main()
