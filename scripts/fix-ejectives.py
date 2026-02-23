#!/usr/bin/env python3
"""Replace soft-sign ejective digraphs with palochka in Kaitag lexeme files."""

import os
import re
import glob

REPLACEMENTS = [
    ("пь", "пӏ"),
    ("ть", "тӏ"),
    ("ць", "цӏ"),
    ("чь", "чӏ"),
    ("кь", "кӏ"),
    ("ҡь", "ҡӏ"),
]


def apply_replacements(text):
    for src, dst in REPLACEMENTS:
        text = text.replace(src, dst)
    return text


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_derived_from = False
    in_see_also = False

    for line in lines:
        stripped = line.rstrip('\n')

        # Track context for derived_from and see_also blocks
        if re.match(r'^derived_from:', stripped):
            in_derived_from = True
            in_see_also = False
        elif re.match(r'^see_also:', stripped):
            in_see_also = True
            in_derived_from = False
        elif re.match(r'^\S', stripped):
            # New top-level key resets context
            in_derived_from = False
            in_see_also = False

        # headword field
        m = re.match(r'^(headword:\s+)(.+)$', stripped)
        if m:
            new_val = apply_replacements(m.group(2))
            new_lines.append(m.group(1) + new_val + '\n')
            continue

        # text fields (forms, variants, examples): "  text: ..." or "  - text: ..."
        m = re.match(r'^(\s+(?:- )?text:\s+)(.+)$', stripped)
        if m:
            new_val = apply_replacements(m.group(2))
            new_lines.append(m.group(1) + new_val + '\n')
            continue

        # derived_from / see_also inline: "derived_from: [word1, word2]"
        # or block list items: "  - word"
        if in_derived_from or in_see_also:
            # Inline array on the same line as the key: "key: [a, b, c]"
            m = re.match(r'^(\w.*?:\s+\[)(.+)(\])$', stripped)
            if m:
                new_val = apply_replacements(m.group(2))
                new_lines.append(m.group(1) + new_val + m.group(3) + '\n')
                continue
            # Block list item
            m = re.match(r'^(\s+- )(.+)$', stripped)
            if m:
                new_val = apply_replacements(m.group(2))
                new_lines.append(m.group(1) + new_val + '\n')
                continue

        new_lines.append(line)

    new_content = ''.join(new_lines)
    original_content = ''.join(lines)

    if new_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    lexicon_dir = os.path.join(os.path.dirname(__file__), '..', 'lexicon')
    yaml_files = glob.glob(os.path.join(lexicon_dir, '**', '*.yaml'), recursive=True)

    changed = 0
    for filepath in sorted(yaml_files):
        if process_file(filepath):
            changed += 1
            print(f"Updated: {os.path.relpath(filepath)}")

    print(f"\nDone. {changed}/{len(yaml_files)} files updated.")


if __name__ == '__main__':
    main()
