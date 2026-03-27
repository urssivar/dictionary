#!/usr/bin/env python3
"""Validate dictionary entries: YAML, structure, tags, cross-references, and schema."""

import json
import re
import sys
import yaml
import argparse
import jsonschema
from utils.paths import ROOT
from utils.loaders import load_alphabet, load_valid_tags, resolve_headword_ref
from utils.text import get_first_letter


def main():
    parser = argparse.ArgumentParser(
        description="Validate dictionary entries.")
    parser.add_argument("letters", nargs="*", metavar="LETTER")
    args = parser.parse_args()

    entries_dir = ROOT / 'entries'
    schema_path = ROOT / '.vscode' / 'entry-schema.json'

    _, alphabet_tokens, _, _ = load_alphabet()
    valid_tags = load_valid_tags()

    with open(schema_path, encoding='utf-8') as f:
        schema = json.load(f)

    if args.letters:
        dirs = [entries_dir / letter for letter in args.letters]
        missing = [d for d in dirs if not d.is_dir()]
        if missing:
            for d in missing:
                print(f'letter folder not found: {d.relative_to(ROOT)}')
            sys.exit(1)
    else:
        dirs = sorted(d for d in entries_dir.iterdir() if d.is_dir())

    has_errors = False

    for letter_dir in dirs:
        for yaml_file in sorted(letter_dir.rglob("*.yaml")):
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

            folder = yaml_file.parent.name
            headword = data.get('headword')

            # Headword placement check
            if headword is None:
                errors.append("missing 'headword'")
            else:
                headword_from_filename = re.sub(
                    r'-\d+$', '', yaml_file.stem).replace('_', ' ').lower()
                if headword.lower() != headword_from_filename:
                    errors.append(
                        f"headword/filename mismatch: {headword!r} vs {headword_from_filename!r}")
                expected = get_first_letter(headword.lower(), alphabet_tokens)
                if folder != expected:
                    errors.append(f"wrong folder: '{expected}/'expected")

            # Cross-reference check
            broken = [
                ref
                for field in ('see_also', 'derived_from')
                for ref in data.get(field) or []
                if resolve_headword_ref(ref, alphabet_tokens) is None
            ]
            if broken:
                errors.append(f"broken refs: {', '.join(broken)}")

            # Tags check
            all_tags = list(data.get('tags') or [])
            for defn in data.get('definitions') or []:
                all_tags += defn.get('tags') or []
            unknown = [t for t in all_tags if t not in valid_tags]
            if unknown:
                errors.append(f"unknown tags: {', '.join(unknown)}")

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
