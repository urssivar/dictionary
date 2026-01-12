#!/usr/bin/env python3
"""Convert Kaitag YAML lexicon to CSV for linguistic researchers."""

import csv
import yaml
import sys
from pathlib import Path
from utils import (
    load_alphabet,
    load_grammar_tags,
    mark_stress,
    extract_yaml_variants,
    map_tags,
    simplify_forms,
    create_tokenizer,
    parse_output_path,
    validate_entry,
    print_export_stats,
    load_lexicon_entries
)


def get_tags_stacked(tags, tag_map):
    """Map tags to stacked bilingual format: 'en tags\\nru tags'."""
    if not tags:
        return ''

    mapped = map_tags(tags, tag_map)
    if not mapped:
        return ''

    en_tags = ' '.join([tag['en'] for tag in mapped])
    ru_tags = ' '.join([tag['ru'] for tag in mapped])

    return f"{en_tags}\n{ru_tags}"


def get_headword_with_ipa(entry, vowels):
    """Format headword with IPA: 'headword\\nipa' (or just headword if no IPA)."""
    headword = mark_stress(entry, vowels)

    if 'ipa' in entry and entry['ipa']:
        return f"{headword}\n{entry['ipa']}"

    return headword


def get_definitions(definitions, lang):
    """Extract all translations for given language, newline-separated."""
    if not definitions:
        return ''

    translations = []
    for defn in definitions:
        if 'translation' in defn and lang in defn['translation']:
            trans = defn['translation'][lang]
            if trans:  # Skip None/empty values
                translations.append(str(trans))  # Ensure string conversion

    return '\n'.join(translations)


def get_forms(forms, headword, tags):
    """Use existing simplify_forms(), join with newlines."""
    if not forms:
        return ''

    simplified = simplify_forms(forms, headword, tags)
    return '\n'.join(simplified)


def get_variants(yaml_variants):
    """Use existing extract_yaml_variants(), join with newlines."""
    if not yaml_variants:
        return ''

    variants = extract_yaml_variants(yaml_variants)
    return '\n'.join(variants)


def convert_entry_to_csv(yaml_entry, vowels, tag_map, alphabet_tokens):
    """Convert single YAML entry to CSV row dict."""
    return {
        'letter': '',  # Letter only in separator rows
        'tags': get_tags_stacked(yaml_entry.get('tags', []), tag_map),
        'headword': get_headword_with_ipa(yaml_entry, vowels),
        'eng': get_definitions(yaml_entry.get('definitions', []), 'en'),
        'rus': get_definitions(yaml_entry.get('definitions', []), 'ru'),
        'forms': get_forms(
            yaml_entry.get('forms', []),
            yaml_entry['headword'],
            yaml_entry.get('tags', [])
        ),
        'variants': get_variants(yaml_entry.get('variants', []))
    }


def main():
    # Use new utility for output path
    output_file = parse_output_path('dictionary.csv')

    # Load data files
    alphabet, alphabet_tokens, vowels = load_alphabet()
    tag_map = load_grammar_tags()
    sorting_key = create_tokenizer(alphabet, alphabet_tokens)

    # Load all entries using new utility
    entries_by_letter, total_entries, skipped_entries = load_lexicon_entries(
        alphabet,
        validate_fn=validate_entry
    )

    # Process all letters
    all_entries = []
    for letter in alphabet:
        if letter not in entries_by_letter:
            continue

        # Convert entries
        entries = [
            convert_entry_to_csv(entry, vowels, tag_map, alphabet_tokens)
            for entry in entries_by_letter[letter]
        ]

        # Sort entries
        entries.sort(key=lambda e: sorting_key({'headword': e['headword'].split('\n')[0]}))

        # Add letter separator row
        all_entries.append({
            'letter': letter, 'tags': '', 'headword': '',
            'eng': '', 'rus': '', 'forms': '', 'variants': ''
        })

        # Add all entries for this letter
        all_entries.extend(entries)

    # Write output CSV
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ['letter', 'tags', 'headword', 'eng', 'rus', 'forms', 'variants']
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_entries)

    # Print stats using new utility
    print_export_stats(total_entries, skipped_entries, output_path)


if __name__ == '__main__':
    main()
