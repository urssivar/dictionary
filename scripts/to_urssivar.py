#!/usr/bin/env python3
"""Convert Kaitag YAML entries to JSON for static website (optimized format)."""

import json
from utils.paths import ROOT
from utils.meta import letters, export_tag_map
from utils.entries import load_entries, clean_id, resolve_headword_ref
from utils.text import sorting_key, mark_stress


def resolve_headword_links(headword_refs):
    result = []
    for ref in headword_refs or []:
        path = resolve_headword_ref(ref)
        if path is None:
            print(f"⚠️ ref not found: {ref}")
            continue
        if path is not True:
            result.append({
                'headword': clean_id(ref),
                'link': f"{path.parent.name}#{path.stem}"
            })
    return result


def transform_definitions(definitions):
    if not definitions:
        return []

    result = []
    for defn in definitions:
        def_obj = {}
        if 'translation' in defn:
            def_obj['translation'] = defn['translation']
        if defn.get('examples'):
            def_obj['examples'] = [
                {'text': ex['text'], 'translation': ex['translation']}
                for ex in defn['examples']
                if 'translation' in ex
            ]
        if 'aliases' in defn:
            def_obj['aliases'] = defn['aliases']
        if 'note' in defn:
            def_obj['note'] = defn['note']
        if def_obj:
            result.append(def_obj)

    return result


def convert_entry(yaml_entry):
    tag_map = export_tag_map()
    result = {
        'id': yaml_entry['id'],
        'headword': mark_stress(yaml_entry),
    }

    if 'tags' in yaml_entry:
        mapped = [{'en': tag_map[t]['en'], 'ru': tag_map[t]['ru']}
                  for t in yaml_entry['tags'] if t in tag_map]
        if mapped:
            result['tags'] = mapped

    if 'forms' in yaml_entry:
        forms = []
        for form in yaml_entry['forms']:
            text = form['text']
            if 'obl' in form['gloss']:
                text += '-'
            forms.append(text)
        if forms:
            result['forms'] = forms

    definitions = transform_definitions(yaml_entry['definitions'])
    if definitions:
        result['definitions'] = definitions

    if yaml_entry.get('variants'):
        result['variants'] = yaml_entry['variants']
    if 'etymology' in yaml_entry:
        result['etymology'] = yaml_entry['etymology']
    if 'note' in yaml_entry:
        result['note'] = yaml_entry['note']

    if yaml_entry.get('derived_from'):
        links = resolve_headword_links(yaml_entry['derived_from'])
        if links:
            result['derived_from'] = links

    if yaml_entry.get('see_also'):
        links = resolve_headword_links(yaml_entry['see_also'])
        if links:
            result['see_also'] = links

    return result


def main():
    output_path = ROOT / 'export' / 'dictionary-urssivar.json'

    entries_by_letter, total_entries, skipped_entries = load_entries()

    converted_entries = {}
    for letter in letters():
        converted = [convert_entry(entry)
                     for entry in entries_by_letter.get(letter, [])]
        converted.sort(key=sorting_key)
        converted_entries[letter] = converted

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(converted_entries, f, ensure_ascii=False, indent=2)

    skipped = f", {skipped_entries} skipped" if skipped_entries else ""
    print(f"\n✔️ {total_entries} entries{skipped} → {output_path}")
    for letter, entries in converted_entries.items():
        print(f"  {letter}: {len(entries)}")


if __name__ == '__main__':
    main()
