#!/usr/bin/env python3
"""Text processing utilities for dictionary entries."""


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
