#!/usr/bin/env python3

import yaml


def load_valid_tags(data_dir):
    with open(data_dir / 'tags.yaml', 'r', encoding='utf-8') as f:
        taxonomy = yaml.safe_load(f)
    return {k for cat in taxonomy.values() if isinstance(cat, dict) for k in cat}


def validate_tags(lexicon_dir, data_dir):
    valid_tags = load_valid_tags(data_dir)
    has_errors = False

    for yaml_file in sorted(lexicon_dir.rglob("*.yaml")):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            has_errors = True
            print(f"❌ YAML parse error: {e}\n  {yaml_file.relative_to(lexicon_dir.parent)}:1")
            continue

        if not data or not isinstance(data, dict):
            continue

        ref = yaml_file.relative_to(lexicon_dir.parent)
        for tag in data.get('tags') or []:
            if tag not in valid_tags:
                has_errors = True
                print(f"❌ unknown tag '{tag}'\n  {ref}:1")
        for defn in data.get('definitions') or []:
            if isinstance(defn, dict):
                for tag in defn.get('tags') or []:
                    if tag not in valid_tags:
                        has_errors = True
                        print(f"❌ unknown tag '{tag}' (definition)\n  {ref}:1")

    if has_errors:
        return False
    return True
