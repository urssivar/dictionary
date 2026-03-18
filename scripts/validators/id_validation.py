#!/usr/bin/env python3

import yaml
from pathlib import Path
from collections import defaultdict


def validate_ids(lexicon_dir):
    id_to_files = defaultdict(list)
    has_errors = False

    for yaml_file in lexicon_dir.rglob("*.yaml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            has_errors = True
            print(f"❌ YAML parse error: {e}\n  {yaml_file.relative_to(lexicon_dir.parent)}:1")
            continue
        if not data:
            continue
        if 'id' not in data or not data['id']:
            has_errors = True
            print(f"❌ missing 'id'\n  {yaml_file.relative_to(lexicon_dir.parent)}:1")
        else:
            id_to_files[data['id']].append(yaml_file)

    for entry_id, files in id_to_files.items():
        if len(files) > 1:
            has_errors = True
            print(f"❌ ID collision '{entry_id}'")
            for file in files:
                print(f"  {file.relative_to(lexicon_dir.parent)}:1")

    if has_errors:
        return False
    return True
