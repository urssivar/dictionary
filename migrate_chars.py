#!/usr/bin/env python3
"""Replace ә→ә, Ә→Ә in Kaitag-language fields and filenames."""

import os
import sys
from pathlib import Path
from ruamel.yaml import YAML

TRANS = str.maketrans({'ә': 'ә', 'Ә': 'Ә'})


def r(s):
    return s.translate(TRANS) if isinstance(s, str) else s


def process(data):
    if 'headword' in data:
        data['headword'] = r(data['headword'])
    for form in data.get('forms') or []:
        if 'text' in form:
            form['text'] = r(form['text'])
    # Mutate in-place to preserve ruamel's flow/block style flag on the sequence
    for key in ('variants', 'see_also', 'derived_from'):
        if key in data:
            seq = data[key]
            for i in range(len(seq)):
                seq[i] = r(seq[i])
    for defn in data.get('definitions') or []:
        if not isinstance(defn, dict):
            continue
        for ex in defn.get('examples') or []:
            if 'text' in ex:
                ex['text'] = r(ex['text'])


yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096  # prevent line wrapping
yaml.indent(mapping=2, sequence=4, offset=2)

entries_root = Path(__file__).parent / 'entries'
renamed = 0
modified = 0

errors = []

for yaml_file in sorted(entries_root.rglob('*.yaml')):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
    except Exception as e:
        errors.append((yaml_file, str(e)))
        continue

    if data is None:
        continue

    process(data)

    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
    modified += 1

    # rename file if needed
    new_name = yaml_file.name.translate(TRANS)
    if new_name != yaml_file.name:
        new_path = yaml_file.parent / new_name
        yaml_file.rename(new_path)
        renamed += 1

# Rename letter directories
for letter_dir in sorted(entries_root.iterdir()):
    if letter_dir.is_dir():
        new_name = letter_dir.name.translate(TRANS)
        if new_name != letter_dir.name:
            letter_dir.rename(letter_dir.parent / new_name)
            renamed += 1

print(f"Modified {modified} files, renamed {renamed} files.")
if errors:
    print(f"\nSkipped {len(errors)} files with parse errors:")
    for path, err in errors:
        print(f"  {path}: {err}")
