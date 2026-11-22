#!/usr/bin/env python3
"""Create a new dictionary entry file."""

import sys
from utils.paths import ROOT
from utils.text import first_letter


def main():
    if len(sys.argv) < 2:
        print("Usage: python d.py new <headword>")
        sys.exit(1)

    headword = sys.argv[1]

    letter_dir = ROOT / 'entries' / first_letter(headword)
    letter_dir.mkdir(parents=True, exist_ok=True)

    slug = headword.replace(' ', '_')
    path = letter_dir / f"{slug}.yaml"
    if path.exists():
        n = 2
        while (letter_dir / f"{slug}-{n}.yaml").exists():
            n += 1
        path = letter_dir / f"{slug}-{n}.yaml"

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
