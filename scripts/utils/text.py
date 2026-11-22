#!/usr/bin/env python3
"""Text helpers over the Kaitag alphabet (read from utils.meta's cached loaders)."""
from utils.meta import load_alphabet, letters


def first_letter(word):
    """First grapheme of a headword, skipping leading non-letters: '-деҳ' → 'д'."""
    word = word.lower()
    chars = {c for g in letters() for c in g}
    i = 0
    while i < len(word) and word[i] not in chars:
        i += 1
    word = word[i:]
    for t in sorted(letters(), key=len, reverse=True):
        if word.startswith(t):
            return t
    print(f'⚠️ unknown first letter in "{word}"')
    return word[0] if word else ''


def _tokenize(word):
    word = word.lower()
    toks = sorted(letters(), key=len, reverse=True)
    out = []
    i = 0
    while i < len(word):
        tok = next((t for t in toks if word.startswith(t, i)), word[i])
        out.append(tok)
        i += len(tok)
    return out


def sorting_key(entry):
    """Sort by letters only, so affixes cluster with their base word."""
    order = {g: i for i, g in enumerate(letters())}
    return [order[t] for t in _tokenize(entry['id'].lower()) if t in order]


def mark_stress(entry):
    ipa = entry.get('ipa')
    if not ipa:
        return entry['headword']

    alpha = load_alphabet()['alphabet']
    vowels = {info['ipa']: g for g, info in alpha.items() if info['type'] == 'vowel'}
    headword = entry['headword']
    ipa = ipa.replace('ˈ', "'").replace('ˌ', "'")

    # Tokenize IPA into (text, type); vowel tokens longest-first (ʷa → о)
    vowel_tokens = sorted(vowels, key=len, reverse=True)
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
            tok = next((t for t in vowel_tokens if ipa.startswith(t, i)), None)
            if tok:
                tokens.append((tok, 'vowel'))
                i += len(tok)
            else:
                tokens.append((ipa[i], 'other'))
                i += 1

    # Drop stress markers in monosyllabic (space/dash-delimited) segments
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

    # Insert combining accent after the stressed vowel in the headword
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
