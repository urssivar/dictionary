#!/usr/bin/env python3
"""Convert Kaitag YAML entries to CSV for linguistic researchers."""

import csv
import re
from utils import ROOT, load_alphabet, load_entries


def normalize_ref(ref):
    return re.sub(r'-\d+$', '', ref).replace('_', ' ')


FIELDNAMES = ['headword', 'ipa', 'tags', 'forms', 'translation',
              'examples', 'note', 'variants', 'derived_from', 'see_also']


def fmt_translation(text, aliases=None):
    """Format a single translation with optional aliases in parentheses."""
    if aliases:
        return f"{text} ({', '.join(aliases)})"
    return text


def convert_entry(entry):
    defs = entry.get('definitions', [])
    multi = len(defs) > 1

    # tags: entry-level first, then each sense's tags on its own line
    tags_parts = []
    entry_tags = entry.get('tags', [])
    if entry_tags:
        tags_parts.append(', '.join(entry_tags))
    for d in defs:
        if d.get('tags'):
            tags_parts.append(', '.join(d['tags']))

    # forms: text (gloss) pairs
    forms_parts = []
    for form in entry.get('forms', []):
        text = form['text']
        if 'obl' in form['gloss']:
            text += '-'
        forms_parts.append(f'{text} ({form["gloss"]})')

    # translation: numbered blocks if multi-sense
    trans_blocks = []
    for i, d in enumerate(defs, 1):
        t = d.get('translation', {})
        aliases = d.get('aliases', {})
        en = fmt_translation(t.get('en', ''), aliases.get('en'))
        ru = fmt_translation(t.get('ru', ''), aliases.get('ru'))
        if multi:
            trans_blocks.append(f'{i}.\n{en}\n{ru}')
        else:
            trans_blocks.append(f'{en}\n{ru}')

    # examples: numbered blocks if multi-sense
    ex_blocks = []
    for i, d in enumerate(defs, 1):
        examples = d.get('examples', [])
        if not examples:
            continue
        lines = []
        for ex in examples:
            t = ex.get('translation', {})
            lines.append(f'{ex["text"]}\n{t.get("en", "")}\n{t.get("ru", "")}')
        sense_block = '\n\n'.join(lines)
        if multi:
            ex_blocks.append(f'{i}.\n{sense_block}')
        else:
            ex_blocks.append(sense_block)

    # note: merge entry note + etymology, then sense notes
    note_parts = []
    entry_note = entry.get('note', {})
    etymology = entry.get('etymology', {})
    # entry-level: note first, then etymology, each as en\nru
    top_lines = []
    for src in [entry_note, etymology]:
        if src:
            top_lines.append(f'{src.get("en", "")}\n{src.get("ru", "")}')
    if top_lines:
        note_parts.append('\n\n'.join(top_lines))
    # sense-level notes
    for i, d in enumerate(defs, 1):
        if d.get('note'):
            n = d['note']
            note_parts.append(f'{i}.\n{n.get("en", "")}\n{n.get("ru", "")}')

    return {
        'headword': entry.get('headword', ''),
        'ipa': entry.get('ipa', ''),
        'tags': '\n'.join(tags_parts),
        'forms': '\n'.join(forms_parts),
        'translation': '\n\n'.join(trans_blocks),
        'examples': '\n\n'.join(ex_blocks),
        'note': '\n\n'.join(note_parts),
        'variants': ', '.join(entry.get('variants') or []),
        'derived_from': ', '.join(normalize_ref(r) for r in (entry.get('derived_from') or [])),
        'see_also': ', '.join(normalize_ref(r) for r in (entry.get('see_also') or [])),
    }


def main():
    output_path = ROOT / 'export' / 'dictionary.csv'

    alphabet, _, _, sorting_key = load_alphabet()
    entries_by_letter, total_entries, skipped_entries = load_entries(alphabet)

    all_entries = []
    for letter in alphabet:
        raw = entries_by_letter.get(letter, [])
        raw.sort(key=sorting_key)
        for e in raw:
            try:
                all_entries.append(convert_entry(e))
            except Exception as err:
                skipped_entries += 1
                print(f"⚠️ {e.get('headword', '?')}: {err}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(all_entries)

    skipped = f", {skipped_entries} skipped" if skipped_entries else ""
    print(f"\n✔️ {total_entries} entries{skipped} → {output_path}")


if __name__ == '__main__':
    main()
