#!/usr/bin/env python3


def get_first_letter(word, alphabet_tokens):
    word = word.lower()
    for letter in alphabet_tokens:
        if word.startswith(letter):
            return letter
    print(f'⚠️ unknown first letter in "{word}"')
    return word[0]


def mark_stress(entry, vowels):
    if 'ipa' not in entry or not entry['ipa']:
        return entry['headword']

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


def create_tokenizer(alphabet, alphabet_tokens):
    alphabet_full = ['-', ' ', '_'] + alphabet
    letter_order = {letter: i for i, letter in enumerate(alphabet_full)}

    def tokenize(word):
        i = 0
        tokens = []
        word = word.lower()
        while i < len(word):
            matched = False
            for letter in alphabet_tokens:
                if word[i:].startswith(letter):
                    tokens.append(letter)
                    i += len(letter)
                    matched = True
                    break
            if not matched:
                tokens.append(word[i])
                i += 1
        return tokens

    def sorting_key(entry):
        headword = entry['id'].lower()
        try:
            return [letter_order.get(t, 999) for t in tokenize(headword)]
        except Exception:
            return [0]

    return sorting_key
