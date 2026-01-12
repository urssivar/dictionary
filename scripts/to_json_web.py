#!/usr/bin/env python3
"""Convert Kaitag YAML lexicon to JSON for static website (optimized format)."""

import json
import yaml
import sys
import re
from pathlib import Path
from utils import (
    load_alphabet,
    load_grammar_tags,
    get_first_letter,
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


def resolve_headword_link(headword_ref, lexicon_dir, alphabet_tokens):
    """Resolve a headword reference to {headword, link} format.

    Args:
        headword_ref: Reference string (e.g., "хъан", "хъан-2", "*root")
        lexicon_dir: Path to lexicon directory
        alphabet_tokens: Alphabet tokens for letter extraction

    Returns:
        Dict with {headword, link} or None if should be skipped/not found
    """
    # Skip reconstructed roots
    if headword_ref.startswith('*'):
        return None

    # Extract clean headword (remove homonym suffix for display)
    clean_headword = re.sub(r'-\d+$', '', headword_ref)

    # Get first letter
    letter = get_first_letter(headword_ref, alphabet_tokens)

    # Build file path (use full reference including homonym suffix)
    yaml_file = lexicon_dir / letter / f"{headword_ref}.yaml"

    # Read file to get ID
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            if 'id' not in yaml_data:
                print(f"Warning: No ID found in {yaml_file}")
                return None

            return {
                'headword': clean_headword,
                'link': f"{letter}#{yaml_data['id']}"
            }
    except FileNotFoundError:
        print(f"Warning: Referenced file not found: {yaml_file}")
        return None
    except Exception as e:
        print(f"Error reading {yaml_file}: {e}")
        return None


def resolve_headword_links(headword_refs, lexicon_dir, alphabet_tokens):
    """Resolve a list of headword references to link objects.

    Args:
        headword_refs: List of headword reference strings
        lexicon_dir: Path to lexicon directory
        alphabet_tokens: Alphabet tokens for letter extraction

    Returns:
        List of {headword, link} objects
    """
    if not headword_refs:
        return []

    result = []
    for ref in headword_refs:
        link_obj = resolve_headword_link(ref, lexicon_dir, alphabet_tokens)
        if link_obj:
            result.append(link_obj)

    return result


def transform_definitions(definitions):
    """Convert YAML definitions to JSON with bilingual structure (low-level i18n).

    Nearly 1:1 conversion - keeps bilingual objects at leaf level.
    """
    if not definitions:
        return []

    result = []
    for defn in definitions:
        def_obj = {}

        # Translation (bilingual)
        if 'translation' in defn:
            def_obj['translation'] = defn['translation']

        # Examples (nested translation structure)
        if 'examples' in defn and defn['examples']:
            def_obj['examples'] = []
            for ex in defn['examples']:
                ex_obj = {'text': ex['text']}
                if 'translation' in ex:
                    ex_obj['translation'] = ex['translation']
                def_obj['examples'].append(ex_obj)

        # Aliases (bilingual arrays)
        if 'aliases' in defn:
            def_obj['aliases'] = defn['aliases']

        # Note (bilingual text)
        if 'note' in defn:
            def_obj['note'] = defn['note']

        if def_obj:  # Only add if not empty
            result.append(def_obj)

    return result


def convert_entry(yaml_entry, vowels, tag_map, lexicon_dir, alphabet_tokens):
    """Convert single YAML entry to JSON format."""
    # Validate required fields
    if 'id' not in yaml_entry or 'headword' not in yaml_entry or 'definitions' not in yaml_entry:
        return None

    result = {
        'id': yaml_entry['id'],
        'headword': mark_stress(yaml_entry, vowels),
    }

    # Tags (filter to grammar tags, map to bilingual)
    if 'tags' in yaml_entry:
        mapped_tags = map_tags(yaml_entry['tags'], tag_map)
        if mapped_tags:
            result['tags'] = mapped_tags

    # Forms (text only, with special processing)
    if 'forms' in yaml_entry:
        forms = simplify_forms(
            yaml_entry['forms'],
            yaml_entry['headword'],
            yaml_entry.get('tags', [])
        )
        if forms:
            result['forms'] = forms

    # Definitions (bilingual structure)
    definitions = transform_definitions(yaml_entry['definitions'])
    if definitions:
        result['definitions'] = definitions

    # Variants (from YAML variants field only - note extraction deprecated)
    if 'variants' in yaml_entry and yaml_entry['variants']:
        variants = extract_yaml_variants(yaml_entry['variants'])
        if variants:
            result['variants'] = variants

    # Etymology (bilingual text)
    if 'etymology' in yaml_entry:
        result['etymology'] = yaml_entry['etymology']

    # Note (bilingual text)
    if 'note' in yaml_entry:
        result['note'] = yaml_entry['note']

    # Derived from (cross-references with links)
    if 'derived_from' in yaml_entry and yaml_entry['derived_from']:
        derived_links = resolve_headword_links(
            yaml_entry['derived_from'], lexicon_dir, alphabet_tokens)
        if derived_links:
            result['derived_from'] = derived_links

    # See also (cross-references with links)
    if 'see_also' in yaml_entry and yaml_entry['see_also']:
        see_also_links = resolve_headword_links(
            yaml_entry['see_also'], lexicon_dir, alphabet_tokens)
        if see_also_links:
            result['see_also'] = see_also_links

    return result


def main():
    # Use new utility for output path
    output_file = parse_output_path('dictionary-web.json')

    # Load data files
    alphabet, alphabet_tokens, vowels = load_alphabet()
    tag_map = load_grammar_tags()
    sorting_key = create_tokenizer(alphabet, alphabet_tokens)

    # Load all entries using new utility
    entries_by_letter, total_entries, skipped_entries = load_lexicon_entries(
        alphabet,
        validate_fn=validate_entry
    )

    lexicon_dir = Path(__file__).parent.parent / 'lexicon'

    # Convert and sort entries per letter
    converted_entries = {}
    for letter in alphabet:
        if letter not in entries_by_letter:
            continue

        # Convert entries
        converted = [
            convert_entry(entry, vowels, tag_map, lexicon_dir, alphabet_tokens)
            for entry in entries_by_letter[letter]
        ]

        # Sort entries
        converted.sort(key=sorting_key)
        converted_entries[letter] = converted

    # Write output
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(converted_entries, f, ensure_ascii=False, indent=2)

    # Print stats using new utility
    print_export_stats(total_entries, skipped_entries, output_path, converted_entries)


if __name__ == '__main__':
    main()
