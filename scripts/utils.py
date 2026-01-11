#!/usr/bin/env python3
"""Shared utilities for dictionary export scripts."""

import yaml
import re
from pathlib import Path


def load_alphabet():
    """Load Kaitag alphabet and derive vowel mappings from it."""
    alphabet_file = Path(__file__).parent.parent / 'data' / 'alphabet.yaml'
    with open(alphabet_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Extract grapheme list in alphabetical order (YAML preserves order)
    alphabet = list(data['alphabet'].keys())

    # Create length-sorted version for tokenization only
    alphabet_tokens = sorted(['-', ' '] + alphabet, key=len, reverse=True)

    # Derive vowel mappings (IPA → Cyrillic) from alphabet
    vowels = {}
    for grapheme, info in data['alphabet'].items():
        if info['type'] == 'vowel':
            vowels[info['ipa']] = grapheme

    return alphabet, alphabet_tokens, vowels


def load_grammar_tags():
    """Load grammar tag mappings from data file.

    Only loads tags meant for JSON export (part of speech + cls/pl).
    Excludes grammatical features (vb, tr, ntr) which are internal-only.
    """
    tags_file = Path(__file__).parent.parent / 'data' / 'tags.yaml'
    with open(tags_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Tags to include in JSON export (part of speech + cls/pl)
    exportable_tags = {
        'n', 'v', 'adj', 'adv', 'conj', 'prep', 'post',
        'intj', 'pro', 'num', 'cop', 'ptcl', 'det', 'cls', 'pl'
    }

    # Convert to simple dict: short_form -> {en:, ru:}
    tag_map = {}
    for short_form, tag_data in data['grammar'].items():
        if short_form in exportable_tags:
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


def extract_yaml_variants(yaml_variants):
    """Extract variant text from YAML variants field.

    Args:
        yaml_variants: List of {text: "..."} objects from YAML

    Returns:
        List of variant strings
    """
    if not yaml_variants:
        return []

    return [v['text'] for v in yaml_variants if 'text' in v]


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


def simplify_forms(forms, headword, tags):
    """Extract and process forms with special handling for compound verbs and oblique stems."""
    if not forms:
        return []

    # Check if this is a compound verb (verb tag + space in headword)
    is_compound_verb = 'v' in tags and ' ' in headword

    result = []
    for form in forms:
        text = form.get('text', '')
        if not text or text == headword:
            continue

        # Compound verb: collapse first part to tilde
        if is_compound_verb:
            text = '~ ' + text.split()[-1]

        # Oblique stem: append dash
        if form.get('gloss') == 'obl':
            text += '-'

        result.append(text)

    return result


def create_tokenizer(alphabet, alphabet_tokens):
    """Create a tokenizer function for sorting."""
    alphabet_full = ['-', ' '] + alphabet  # alphabetical order for sorting
    letter_order = {letter: i for i, letter in enumerate(alphabet_full)}

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
