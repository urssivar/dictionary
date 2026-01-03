#!/usr/bin/env python3
"""Convert Kaitag YAML lexicon to JSON for static website."""

import json
import yaml
import sys
import re
from pathlib import Path
from collections import defaultdict


def load_alphabet():
    """Load Kaitag alphabet and derive vowel mappings from it."""
    alphabet_file = Path(__file__).parent.parent / 'data' / 'alphabet.yaml'
    with open(alphabet_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Extract grapheme list from alphabet dict
    alphabet = list(data['alphabet'].keys())
    alphabet = sorted(alphabet, key=len, reverse=True)

    # Derive vowel mappings (IPA → Cyrillic) from alphabet
    vowels = {}
    for grapheme, info in data['alphabet'].items():
        if info['type'] == 'vowel':
            vowels[info['ipa']] = grapheme

    return alphabet, vowels


def load_grammar_tags():
    """Load grammar tag mappings from data file."""
    tags_file = Path(__file__).parent.parent / 'data' / 'tags.yaml'
    with open(tags_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Convert to simple dict: short_form -> {en:, ru:}
    tag_map = {}
    for short_form, tag_data in data['grammar'].items():
        tag_map[short_form] = {
            'en': tag_data['en'],
            'ru': tag_data['ru']
        }
    return tag_map


def get_first_letter(word, alphabet_tokens):
    """Get first letter, respecting digraphs."""
    word = word.lower()
    for letter in alphabet_tokens:
        if word.startswith(letter):
            return letter
    print(f'Warning: unknown first letter in "{word}"')
    return word[0]


def mark_stress(entry, vowels):
    """Add stress marks to headword based on IPA.

    Ported from transformer.ipynb cell-3.
    """
    if 'ipa' not in entry or not entry['ipa']:
        return entry['headword']

    headword = entry['headword']
    ipa = entry['ipa'].replace('ˈ', "'").replace('ˌ', "'")

    # Count vowels helper
    def count_vowels(s):
        return sum(1 for char in s if char in vowels)

    # Remove predictable stresses (single vowel in word part)
    i_stress = -1
    i_word = 0
    v_count = 0
    i_char = 0

    while i_char < len(ipa):
        char = ipa[i_char]
        if char == "'":
            i_stress = i_char
        elif char in vowels:
            v_count += 1
        if char in ' -' or i_char == len(ipa) - 1:
            if v_count <= 1 and i_stress >= i_word:
                ipa = ipa[:i_stress] + ipa[i_stress + 1:]
                i_char -= 1
            i_word = i_char + 1
            v_count = 0
        i_char += 1

    if "'" not in ipa:
        return headword

    # Apply stress marks to headword
    i_vowel = -1
    needs_stress = False

    for char in ipa:
        if char == "'":
            needs_stress = True
        if char in vowels:
            i_vowel = headword.find(vowels[char], i_vowel + 1)
            if i_vowel == -1:
                # Vowel not found, return original
                return entry['headword']
            if needs_stress:
                headword = headword[:i_vowel + 1] + \
                    '\u0301' + headword[i_vowel + 1:]
                i_vowel += 1
                needs_stress = False

    return headword


def extract_variants(note):
    """Extract variants from note field using markdown italic pattern.

    Ported from transformer.ipynb cell-2.
    """
    if not note or 'en' not in note:
        return []

    text = note['en']
    matches = re.findall(r'\*([^*]+)\*', text)
    return [m.strip() for m in matches]


def map_tags(tags, tag_map):
    """Map tags to bilingual format, filter to grammar tags only.

    Returns array of {en:, ru:} objects.
    """
    if not tags:
        return []

    result = []
    for tag in tags:
        if tag in tag_map:
            result.append({
                'en': tag_map[tag]['en'],
                'ru': tag_map[tag]['ru']
            })

    return result


def simplify_forms(forms, headword):
    """Extract text from forms, skip gloss and forms matching headword."""
    if not forms:
        return []

    result = []
    for form in forms:
        text = form.get('text', '')
        if text and text != headword:
            result.append(text)

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

        if def_obj:  # Only add if not empty
            result.append(def_obj)

    return result


def convert_entry(yaml_entry, vowels, tag_map):
    """Convert single YAML entry to JSON format."""
    # Validate required fields
    if 'id' not in yaml_entry or 'headword' not in yaml_entry or 'definitions' not in yaml_entry:
        return None

    result = {
        'id': yaml_entry['id'],
        'headword': mark_stress(yaml_entry, vowels),
    }

    # Optional: IPA
    if 'ipa' in yaml_entry:
        result['ipa'] = yaml_entry['ipa']

    # Tags (filter to grammar tags, map to bilingual)
    if 'tags' in yaml_entry:
        mapped_tags = map_tags(yaml_entry['tags'], tag_map)
        if mapped_tags:
            result['tags'] = mapped_tags

    # Forms (text only, no gloss)
    if 'forms' in yaml_entry:
        forms = simplify_forms(yaml_entry['forms'], yaml_entry['headword'])
        if forms:
            result['forms'] = forms

    # Definitions (bilingual structure)
    definitions = transform_definitions(yaml_entry['definitions'])
    if definitions:
        result['definitions'] = definitions

    # Variants (extracted from note)
    if 'note' in yaml_entry:
        variants = extract_variants(yaml_entry['note'])
        if variants:
            result['variants'] = variants

    return result


def create_tokenizer(alphabet_tokens):
    """Create a tokenizer function for sorting."""
    letter_order = {letter: i for i, letter in enumerate(
        ['-', ' '] + alphabet_tokens)}

    def tokenize(word):
        i = 0
        tokens = []
        word = word.lower()
        while i < len(word):
            # Find longest matching letter
            matched = False
            for letter in alphabet_tokens:
                if word[i:].startswith(letter):
                    tokens.append(letter)
                    i += len(letter)
                    matched = True
                    break
            if not matched:
                # Unknown character, use as-is
                tokens.append(word[i])
                i += 1
        return tokens

    def sorting_key(entry):
        headword = entry['headword'].lower()
        # Remove combining accent marks for sorting
        headword = headword.replace('\u0301', '')
        try:
            return [letter_order.get(token, 999) for token in tokenize(headword)]
        except Exception:
            return [0]

    return sorting_key


def main():
    # Default output to data/dictionary.json if not specified
    if len(sys.argv) < 2:
        output_file = Path(__file__).parent.parent / 'data' / 'dictionary.json'
    else:
        output_file = sys.argv[1]

    # Load data files
    alphabet_tokens, vowels = load_alphabet()
    tag_map = load_grammar_tags()
    alphabet = [t for t in alphabet_tokens if t not in ['-', ' ']]

    # Create sorting function
    sorting_key = create_tokenizer(alphabet_tokens)

    # Process all letters
    output = {}
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

                converted = convert_entry(yaml_data, vowels, tag_map)
                if converted:
                    entries.append(converted)
                    total_entries += 1
                else:
                    skipped_entries += 1
                    print(
                        f"Warning: Skipped {yaml_file.name} (missing required fields)")

            except Exception as e:
                skipped_entries += 1
                print(f"Error processing {yaml_file.name}: {e}")

        # Sort entries
        entries.sort(key=sorting_key)
        output[letter] = entries

    # Write output JSON
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Report statistics
    print(f"\nConversion complete!")
    print(f"Total entries: {total_entries}")
    print(f"Skipped entries: {skipped_entries}")
    print(f"Output written to: {output_path}")

    # Entries per letter
    print(f"\nEntries per letter:")
    for letter in alphabet:
        if letter in output:
            print(f"  {letter}: {len(output[letter])}")


if __name__ == '__main__':
    main()
