#!/usr/bin/env python3
"""Validate ID presence and uniqueness across all entries."""

import yaml
from pathlib import Path
from collections import defaultdict


def validate_ids(lexicon_dir):
    """Check for missing and duplicate IDs. Returns None on failure, True on success."""
    id_to_files = defaultdict(list)
    has_errors = False

    # Scan all YAML files
    for yaml_file in lexicon_dir.rglob("*.yaml"):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        if not data:
            continue
        if 'id' not in data or not data['id']:
            has_errors = True
            print(f"ERROR: missing 'id'\n  {yaml_file.relative_to(lexicon_dir.parent)}:1")
        else:
            id_to_files[data['id']].append(yaml_file)

    # Check for collisions
    for entry_id, files in id_to_files.items():
        if len(files) > 1:
            has_errors = True
            print(f"ERROR: ID collision '{entry_id}'")
            for file in files:
                print(f"  {file.relative_to(lexicon_dir.parent)}:1")

    if has_errors:
        return None  # Failed
    return True  # Success
