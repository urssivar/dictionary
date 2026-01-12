#!/usr/bin/env python3
"""Sorting utilities for dictionary entries."""


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
