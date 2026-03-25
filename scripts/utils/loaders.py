#!/usr/bin/env python3
import re
import yaml
from utils.paths import ROOT
from utils.text import create_tokenizer, get_first_letter

_META_DIR = ROOT / 'meta'

def load_alphabet():
    with open(_META_DIR / 'alphabet.yaml', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    alphabet = list(data['alphabet'].keys())
    alphabet_tokens = sorted(['-', ' '] + alphabet, key=len, reverse=True)

    vowels = {}
    for grapheme, info in data['alphabet'].items():
        if info['type'] == 'vowel':
            vowels[info['ipa']] = grapheme

    sorting_key = create_tokenizer(alphabet, alphabet_tokens)
    return alphabet, alphabet_tokens, vowels, sorting_key


def load_valid_tags():
    with open(_META_DIR / 'tags.yaml', 'r', encoding='utf-8') as f:
        taxonomy = yaml.safe_load(f)
    return {
        k
        for cat in taxonomy.values()
        if isinstance(cat, dict)
        for k in cat
    }


def load_grammar_tags():
    with open(_META_DIR / 'tags.yaml', encoding='utf-8') as f:
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


def resolve_headword_ref(headword_ref, alphabet_tokens):
    if headword_ref.startswith('*'):
        return True
    letter = get_first_letter(headword_ref, alphabet_tokens)
    path = ROOT / 'lexicon' / letter / f"{headword_ref}.yaml"
    return path if path.exists() else None


def load_lexicon_entries(alphabet):
    entries_by_letter = {}
    total_entries = 0
    skipped_entries = 0

    for letter in alphabet:
        letter_dir = ROOT / 'lexicon' / letter
        entries_by_letter[letter] = []

        if not letter_dir.exists():
            continue

        for yaml_file in sorted(letter_dir.glob('*.yaml')):
            try:
                with open(yaml_file, encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                yaml_data['id'] = yaml_file.stem
                entries_by_letter[letter].append(yaml_data)
                total_entries += 1
            except Exception as e:
                skipped_entries += 1
                print(f"{yaml_file.relative_to(ROOT)}\n  • {e}")

    return entries_by_letter, total_entries, skipped_entries
