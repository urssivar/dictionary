#!/usr/bin/env python3
"""Convert Kaitag YAML lexicon to JSON for static website (optimized format)."""

import json
import yaml
import re
from utils import ROOT, load_alphabet, load_grammar_tags, get_first_letter, mark_stress, simplify_forms, load_lexicon_entries


def resolve_headword_link(headword_ref, lexicon_dir, alphabet_tokens):
    if headword_ref.startswith('*'):
        return None

    clean_headword = re.sub(r'-\d+$', '', headword_ref)
    letter = get_first_letter(headword_ref, alphabet_tokens)
    yaml_file = lexicon_dir / letter / f"{headword_ref}.yaml"

    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            if 'id' not in yaml_data:
                print(f"⚠️ no ID in {yaml_file}")
                return None
            return {'headword': clean_headword, 'link': f"{letter}#{yaml_data['id']}"}
    except FileNotFoundError:
        print(f"⚠️ ref not found: {yaml_file}")
        return None
    except Exception as e:
        print(f"❌ {yaml_file}: {e}")
        return None


def resolve_headword_links(headword_refs, lexicon_dir, alphabet_tokens):
    if not headword_refs:
        return []
    return [r for ref in headword_refs if (r := resolve_headword_link(ref, lexicon_dir, alphabet_tokens))]


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
                {'text': ex['text'], **({'translation': ex['translation']} if 'translation' in ex else {})}
                for ex in defn['examples']
            ]
        if 'aliases' in defn:
            def_obj['aliases'] = defn['aliases']
        if 'note' in defn:
            def_obj['note'] = defn['note']
        if def_obj:
            result.append(def_obj)

    return result


def convert_entry(yaml_entry, vowels, tag_map, lexicon_dir, alphabet_tokens):
    if 'id' not in yaml_entry or 'headword' not in yaml_entry or 'definitions' not in yaml_entry:
        return None

    result = {
        'id': yaml_entry['id'],
        'headword': mark_stress(yaml_entry, vowels),
    }

    if 'tags' in yaml_entry:
        mapped = [{'en': tag_map[t]['en'], 'ru': tag_map[t]['ru']} for t in yaml_entry['tags'] if t in tag_map]
        if mapped:
            result['tags'] = mapped

    if 'forms' in yaml_entry:
        forms = simplify_forms(yaml_entry['forms'], yaml_entry['headword'])
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
        links = resolve_headword_links(yaml_entry['derived_from'], lexicon_dir, alphabet_tokens)
        if links:
            result['derived_from'] = links

    if yaml_entry.get('see_also'):
        links = resolve_headword_links(yaml_entry['see_also'], lexicon_dir, alphabet_tokens)
        if links:
            result['see_also'] = links

    return result


def main():
    output_path = ROOT / 'export' / 'dictionary-web.json'

    alphabet, alphabet_tokens, vowels, sorting_key = load_alphabet()
    tag_map = load_grammar_tags()
    entries_by_letter, total_entries, skipped_entries = load_lexicon_entries(alphabet)

    lexicon_dir = ROOT / 'lexicon'

    converted_entries = {}
    for letter in alphabet:
        converted = [
            convert_entry(entry, vowels, tag_map, lexicon_dir, alphabet_tokens)
            for entry in entries_by_letter.get(letter, [])
        ]
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
