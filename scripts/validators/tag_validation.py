#!/usr/bin/env python3
"""Validate tags against taxonomy."""

import yaml
from pathlib import Path


def load_valid_tags(data_dir):
    """Load all valid tags from tags.yaml."""
    tags_file = data_dir / 'tags.yaml'
    with open(tags_file, 'r', encoding='utf-8') as f:
        taxonomy = yaml.safe_load(f)

    valid_tags = set()
    # Extract tag keys from all categories
    for category in taxonomy.values():
        if isinstance(category, dict):
            valid_tags.update(category.keys())

    return valid_tags


def validate_tags(lexicon_dir, data_dir):
    """Check tags against taxonomy. Returns None on failure, True on success."""
    valid_tags = load_valid_tags(data_dir)

    has_errors = False
    for yaml_file in lexicon_dir.rglob("*.yaml"):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

            if not data or not isinstance(data, dict):
                continue

            # Check word-level tags
            if 'tags' in data and data['tags']:
                for tag in data['tags']:
                    if tag not in valid_tags:
                        has_errors = True
                        print(f"ERROR: Unknown tag '{tag}' in {yaml_file}")

            # Check definition-level tags
            if 'definitions' in data and isinstance(data['definitions'], list):
                for definition in data['definitions']:
                    if isinstance(definition, dict) and 'tags' in definition:
                        if definition['tags']:
                            for tag in definition['tags']:
                                if tag not in valid_tags:
                                    has_errors = True
                                    print(f"ERROR: Unknown tag '{tag}' in {yaml_file} (definition)")

    if has_errors:
        return None  # Failed
    return True  # Success
