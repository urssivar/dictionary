#!/usr/bin/env python3
"""Text helpers over the Kaitag alphabet. All read meta via utils.meta's cached
loaders — no alphabet arguments needed anywhere."""
from functools import lru_cache

from utils.meta import load_alphabet


@lru_cache(maxsize=1)
def _graphemes():
    return list(load_alphabet()['alphabet'].keys())


@lru_cache(maxsize=1)
def _tokens():
    return sorted(_graphemes(), key=len, reverse=True)


@lru_cache(maxsize=1)
def _letter_order():
    return {g: i for i, g in enumerate(_graphemes())}


@lru_cache(maxsize=1)
def _letter_chars():
    return frozenset(c for g in _graphemes() for c in g)


@lru_cache(maxsize=1)
def _vowels():
    return {info['ipa']: g for g, info in load_alphabet()['alphabet'].items()
            if info['type'] == 'vowel'}


def first_letter(word):
    """First grapheme of a headword, skipping leading non-letters: '-деҳ' → 'д'."""
    word = word.lower()
    chars = _letter_chars()
    i = 0
    while i < len(word) and word[i] not in chars:
        i += 1
    word = word[i:]
    for t in _tokens():
        if word.startswith(t):
            return t
    print(f'⚠️ unknown first letter in "{word}"')
    return word[0] if word else ''


def tokenize(word):
    word = word.lower()
    toks = _tokens()
    out = []
    i = 0
    while i < len(word):
        tok = next((t for t in toks if word.startswith(t, i)), word[i])
        out.append(tok)
        i += len(tok)
    return out


def sorting_key(entry):
    """Sort by letters only, so affixes cluster with their base word."""
    order = _letter_order()
    return [order[t] for t in tokenize(entry['id'].lower()) if t in order]


def mark_stress(entry):
    if 'ipa' not in entry or not entry['ipa']:
        return entry['headword']

    vowels = _vowels()
    headword = entry['headword']
    ipa = entry['ipa'].replace('ˈ', "'").replace('ˌ', "'")

    # Sort longest-first so multi-char tokens (e.g. ʷa → о) match before substrings
    vowel_tokens = sorted(vowels.keys(), key=len, reverse=True)

    # Tokenize IPA once into (string, type) pairs
    tokens = []
    i = 0
    while i < len(ipa):
        if ipa[i] == "'":
            tokens.append(("'", 'stress'))
            i += 1
        elif ipa[i] in ' -':
            tokens.append((ipa[i], 'sep'))
            i += 1
        else:
            tok = next((t for t in vowel_tokens if ipa[i:i + len(t)] == t), None)
            if tok:
                tokens.append((tok, 'vowel'))
                i += len(tok)
            else:
                tokens.append((ipa[i], 'other'))
                i += 1

    # Pass 1: drop stress markers from monosyllabic words
    stress_at = None
    v_count = 0
    for i, (tok, typ) in enumerate(tokens):
        if typ == 'stress':
            stress_at = i
        elif typ == 'vowel':
            v_count += 1
        if typ == 'sep' or i == len(tokens) - 1:
            if v_count <= 1 and stress_at is not None:
                tokens[stress_at] = ('', 'removed')
            stress_at = None
            v_count = 0

    if not any(typ == 'stress' for _, typ in tokens):
        return headword

    # Pass 2: insert combining accent after the stressed vowel in the headword
    i_vowel = -1
    needs_stress = False
    for tok, typ in tokens:
        if typ == 'stress':
            needs_stress = True
        elif typ == 'vowel':
            i_vowel = headword.find(vowels[tok], i_vowel + 1)
            if i_vowel == -1:
                return entry['headword']
            if needs_stress:
                headword = headword[:i_vowel + 1] + '\u0301' + headword[i_vowel + 1:]
                i_vowel += 1
                needs_stress = False

    return headword
