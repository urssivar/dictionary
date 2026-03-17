#!/usr/bin/env python3
"""Data loading utilities: alphabet, tags, and lexicon entries."""

import sys
import yaml
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent.parent / 'data'
_LEXICON_DIR = Path(__file__).parent.parent.parent / 'lexicon'


def load_alphabet():
    """Load Kaitag alphabet and derive vowel mappings."""
    with open(_DATA_DIR / 'alphabet.yaml', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    alphabet = list(data['alphabet'].keys())
    alphabet_tokens = sorted(['-', ' '] + alphabet, key=len, reverse=True)

    vowels = {}
    for grapheme, info in data['alphabet'].items():
        if info['type'] == 'vowel':
            vowels[info['ipa']] = grapheme

    return alphabet, alphabet_tokens, vowels


def load_grammar_tags():
    """Load grammar tag mappings for export (part of speech + cls/pl only)."""
    with open(_DATA_DIR / 'tags.yaml', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    exportable = {
        'n', 'v', 'adj', 'adv', 'conj', 'prep', 'post',
        'intj', 'pro', 'num', 'cop', 'ptcl', 'det', 'cls', 'pl'
    }

    return {
        short: {'en': tag['en'], 'ru': tag['ru']}
        for short, tag in data['grammar'].items()
        if short in exportable
    }


def load_lexicon_entries(alphabet, validate_fn=None):
    """Load all lexicon entries from YAML files organized by letter.

    Returns (entries_by_letter, total_entries, skipped_entries).
    """
    entries_by_letter = {}
    total_entries = 0
    skipped_entries = 0

    for letter in alphabet:
        letter_dir = _LEXICON_DIR / letter
        entries_by_letter[letter] = []

        if not letter_dir.exists():
            continue

        for yaml_file in sorted(letter_dir.glob('*.yaml')):
            try:
                with open(yaml_file, encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)

                if validate_fn and not validate_fn(yaml_data):
                    skipped_entries += 1
                    print(f"Warning: Skipped {yaml_file.name} (missing required fields)")
                    continue

                entries_by_letter[letter].append(yaml_data)
                total_entries += 1

            except Exception as e:
                skipped_entries += 1
                print(f"Error processing {yaml_file.name}: {e}")

    return entries_by_letter, total_entries, skipped_entries
