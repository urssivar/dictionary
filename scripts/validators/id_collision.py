#!/usr/bin/env python3
"""Validate ID uniqueness across all entries."""

import yaml
from pathlib import Path
from collections import defaultdict


def validate_id_collisions(lexicon_dir):
    """Check for duplicate IDs. Returns None on failure, True on success."""
    id_to_files = defaultdict(list)

    # Scan all YAML files
    for yaml_file in lexicon_dir.rglob("*.yaml"):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data and 'id' in data:
                id_to_files[data['id']].append(yaml_file)

    # Check for collisions
    has_errors = False
    for entry_id, files in id_to_files.items():
        if len(files) > 1:
            has_errors = True
            print(f"ERROR: ID collision '{entry_id}'")
            for file in files:
                print(f"  - {file}")

    if has_errors:
        return None  # Failed
    return True  # Success
