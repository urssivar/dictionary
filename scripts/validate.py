#!/usr/bin/env python3
"""Validate dictionary entries: YAML, structure, tags, cross-references, and schema."""

import json
import sys
import yaml
import argparse
import jsonschema
from utils.paths import ROOT
from utils.meta import valid_tags
from utils.entries import iter_entry_files, entry_id, resolve_headword_ref
from utils.text import first_letter
from utils.etymology import check_etymology


def main():
    parser = argparse.ArgumentParser(
        description="Validate dictionary entries.")
    parser.add_argument("letters", nargs="*", metavar="LETTER")
    args = parser.parse_args()

    entries_dir = ROOT / 'entries'
    schema_path = ROOT / '.vscode' / 'entry-schema.json'

    valid = valid_tags()

    with open(schema_path, encoding='utf-8') as f:
        schema = json.load(f)

    if args.letters:
        missing = [l for l in args.letters if not (entries_dir / l).is_dir()]
        if missing:
            for l in missing:
                print(f'letter folder not found: {entries_dir / l}')
            sys.exit(1)
        files = [(l, p) for l, p in iter_entry_files() if l in args.letters]
    else:
        files = list(iter_entry_files())

    has_errors = False

    for folder, yaml_file in files:
        rel = yaml_file.relative_to(ROOT)
        errors = []

        try:
            with open(yaml_file, encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f'{rel}\n  • YAML parse error: {e}')
            has_errors = True
            continue

        if not data or not isinstance(data, dict):
            continue

        headword = data.get('headword')

        # Headword placement check
        if headword is None:
            errors.append("missing 'headword'")
        else:
            if headword.lower() != entry_id(yaml_file).lower():
                errors.append(
                    f"headword/filename mismatch: {headword!r} vs {entry_id(yaml_file)!r}")
            expected = first_letter(headword.lower())
            if folder != expected:
                errors.append(f"wrong folder: '{expected}/'expected")

        # Cross-reference check
        broken = [
            ref
            for field in ('see_also', 'derived_from')
            for ref in data.get(field) or []
            if resolve_headword_ref(ref) is None
        ]
        if broken:
            errors.append(f"broken refs: {', '.join(broken)}")

        # Tags check
        all_tags = list(data.get('tags') or [])
        for defn in data.get('definitions') or []:
            all_tags += defn.get('tags') or []
        unknown = [t for t in all_tags if t not in valid]
        if unknown:
            errors.append(f"unknown tags: {', '.join(unknown)}")

        # Etymology prose-convention check
        errors += check_etymology(data.get('etymology'))

        # Schema check
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.ValidationError as e:
            errors.append(f"schema: {e.message}")

        if errors:
            has_errors = True
            print(f'{rel}')
            for err in errors:
                print(f"  • {err}")

    print()
    if has_errors:
        print("❌ Validation failed")
        sys.exit(1)
    print("✔️ Valid")


if __name__ == '__main__':
    main()
