#!/usr/bin/env python3
"""Create a new lexicon entry file."""

import sys
from utils.paths import ROOT
from utils.loaders import load_alphabet
from utils.text import get_first_letter

def main():
    if len(sys.argv) < 2:
        print("Usage: python d.py new <headword>")
        sys.exit(1)

    headword = sys.argv[1]
    _, alphabet_tokens, _, _ = load_alphabet()

    letter = get_first_letter(headword, alphabet_tokens)
    letter_dir = ROOT / 'lexicon' / letter
    letter_dir.mkdir(parents=True, exist_ok=True)

    path = letter_dir / f"{headword}.yaml"
    if path.exists():
        n = 2
        while (letter_dir / f"{headword}-{n}.yaml").exists():
            n += 1
        path = letter_dir / f"{headword}-{n}.yaml"

    path.write_text(
        f"headword: {headword}\n"
        f"\n"
        f"definitions:\n"
        f"  - translation:\n"
        f"      en:\n"
        f"      ru:\n",
        encoding='utf-8'
    )
    print(f"{path.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
