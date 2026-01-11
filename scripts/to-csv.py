#!/usr/bin/env python3
"""Convert Kaitag YAML lexicon to CSV for linguistic researchers."""

import csv
import yaml
import sys
from pathlib import Path
from utils import (
    load_alphabet,
    load_grammar_tags,
    get_first_letter,
    mark_stress,
    extract_yaml_variants,
    map_tags,
    simplify_forms,
    create_tokenizer
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
    # Default output to export/dictionary.csv if not specified
    if len(sys.argv) < 2:
        output_file = Path(__file__).parent.parent / 'export' / 'dictionary.csv'
    else:
        output_file = sys.argv[1]

    # Load data files
    alphabet, alphabet_tokens, vowels = load_alphabet()
    tag_map = load_grammar_tags()

    # Create sorting function
    sorting_key = create_tokenizer(alphabet, alphabet_tokens)

    # Process all letters
    all_entries = []
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

                # Validate required fields
                if 'id' not in yaml_data or 'headword' not in yaml_data or 'definitions' not in yaml_data:
                    skipped_entries += 1
                    print(
                        f"Warning: Skipped {yaml_file.name} (missing required fields)")
                    continue

                converted = convert_entry_to_csv(
                    yaml_data, vowels, tag_map, alphabet_tokens)
                entries.append(converted)
                total_entries += 1

            except Exception as e:
                skipped_entries += 1
                print(f"Error processing {yaml_file.name}: {e}")

        # Sort entries for this letter
        entries.sort(key=lambda e: sorting_key({'headword': e['headword'].split('\n')[0]}))

        # Add letter separator row
        all_entries.append({'letter': letter, 'tags': '', 'headword': '', 'eng': '', 'rus': '', 'forms': '', 'variants': ''})

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

    # Report statistics
    print(f"\nConversion complete!")
    print(f"Total entries: {total_entries}")
    print(f"Skipped entries: {skipped_entries}")
    print(f"Output written to: {output_path}")


if __name__ == '__main__':
    main()
