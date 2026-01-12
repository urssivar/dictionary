#!/usr/bin/env python3
"""Alphabet and grammar tag loading utilities."""

import yaml
from pathlib import Path


def load_alphabet():
    """Load Kaitag alphabet and derive vowel mappings from it."""
    alphabet_file = Path(__file__).parent.parent.parent / 'data' / 'alphabet.yaml'
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
    tags_file = Path(__file__).parent.parent.parent / 'data' / 'tags.yaml'
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
