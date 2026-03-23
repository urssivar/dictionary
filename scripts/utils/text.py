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

    i_vowel = -1
    needs_stress = False

    for char in ipa:
        if char == "'":
            needs_stress = True
        if char in vowels:
            i_vowel = headword.find(vowels[char], i_vowel + 1)
            if i_vowel == -1:
                return entry['headword']
            if needs_stress:
                headword = headword[:i_vowel + 1] + '\u0301' + headword[i_vowel + 1:]
                i_vowel += 1
                needs_stress = False

    return headword


def create_tokenizer(alphabet, alphabet_tokens):
    alphabet_full = ['-', ' '] + alphabet
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
        headword = entry['headword'].lower().replace('\u0301', '')
        try:
            return [letter_order.get(t, 999) for t in tokenize(headword)]
        except Exception:
            return [0]

    return sorting_key
