#!/usr/bin/env python3
"""Update IPA fields in Kaitag lexeme files with revised transcription conventions."""

import os
import re
import glob

# Plain consonants that get aspiration when not followed by ː or ʼ
# Order matters: longer sequences first (ts, tʃ before t)
ASPIRATE = [
    ("tʃ", "tʃʰ"),
    ("ts", "tsʰ"),
    ("p",  "pʰ"),
    ("t",  "tʰ"),
    ("k",  "kʰ"),
    ("q",  "qʰ"),
]

SIMPLE = [
    ("v", "β"),
    ("o", "ʷa"),
    ("r", "ɾ"),
    # Fix tie-bar t͡s -> ts (normalise leftover)
    ("t͡", "t"),
]


def transform_ipa(ipa):
    # 1. Simple replacements
    for src, dst in SIMPLE:
        ipa = ipa.replace(src, dst)

    # 2. Aspirate plain stops/affricates: add ʰ when not already followed by ː or ʼ
    # Process longest patterns first (tʃ, ts before t)
    result = []
    i = 0
    while i < len(ipa):
        matched = False
        for src, dst in ASPIRATE:
            if ipa[i:i+len(src)] == src:
                after = ipa[i+len(src):i+len(src)+1]
                if after not in ('ː', 'ʼ', 'ʰ'):
                    result.append(dst)
                else:
                    result.append(src)
                i += len(src)
                matched = True
                break
        if not matched:
            result.append(ipa[i])
            i += 1
    return ''.join(result)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    changed = False
    for line in lines:
        if line.startswith('ipa:'):
            m = re.match(r'^(ipa:\s+)(.+)(\n?)$', line)
            if m:
                new_val = transform_ipa(m.group(2))
                new_line = m.group(1) + new_val + m.group(3)
                if new_line != line:
                    changed = True
                new_lines.append(new_line)
                continue
        new_lines.append(line)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    return changed


def main():
    lexicon_dir = os.path.join(os.path.dirname(__file__), '..', 'lexicon')
    yaml_files = glob.glob(os.path.join(lexicon_dir, '**', '*.yaml'), recursive=True)

    changed = 0
    for filepath in sorted(yaml_files):
        if process_file(filepath):
            changed += 1

    print(f"Done. {changed}/{len(yaml_files)} files updated.")


if __name__ == '__main__':
    main()
