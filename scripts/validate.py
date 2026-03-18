#!/usr/bin/env python3
"""Validate dictionary entries: YAML, structure, IDs, tags, and schema."""

import json
import re
import sys
import yaml
import argparse
import jsonschema
from utils.paths import ROOT
from utils.loaders import load_alphabet, load_valid_tags
from utils.text import get_first_letter


def main():
    parser = argparse.ArgumentParser(
        description="Validate dictionary entries.")
    parser.add_argument("letters", nargs="*", metavar="LETTER")
    args = parser.parse_args()

    lexicon_dir = ROOT / 'lexicon'
    schema_path = ROOT / '.vscode' / 'lexeme-schema.json'

    _, alphabet_tokens, _, _ = load_alphabet()
    valid_tags = load_valid_tags()

    with open(schema_path, encoding='utf-8') as f:
        schema = json.load(f)

    if args.letters:
        dirs = [lexicon_dir / letter for letter in args.letters]
        missing = [d for d in dirs if not d.is_dir()]
        if missing:
            for d in missing:
                print(f"❌ letter folder not found: {d.relative_to(ROOT)}")
            sys.exit(1)
    else:
        dirs = sorted(d for d in lexicon_dir.iterdir() if d.is_dir())

    seen_ids: dict[str, str] = {}
    has_errors = False

    for letter_dir in dirs:
        for yaml_file in sorted(letter_dir.rglob("*.yaml")):
            rel = yaml_file.relative_to(ROOT)
            errors = []

            try:
                with open(yaml_file, encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"❌ {rel}:1\n  • YAML parse error: {e}")
                has_errors = True
                continue

            if not data or not isinstance(data, dict):
                continue

            folder = yaml_file.parent.name
            headword = data.get('headword')

            # Letter folder check
            if headword:
                expected = get_first_letter(headword.lower(), alphabet_tokens)
                if folder != expected:
                    errors.append(f"wrong folder: {headword!r} belongs in '{expected}/'")

            # Headword/filename check
            headword_from_filename = re.sub(
                r'-\d+$', '', yaml_file.stem).lower()
            if headword is None:
                errors.append("missing 'headword'")
            elif headword.lower() != headword_from_filename:
                errors.append(
                    f"headword/filename mismatch: {headword!r} vs filename {headword_from_filename!r}")

            # ID check + inline collision
            entry_id = data.get('id')
            if not entry_id:
                errors.append("missing 'id'")
            elif entry_id in seen_ids:
                errors.append(
                    f"ID collision '{entry_id}' (first seen in {seen_ids[entry_id]})")
            else:
                seen_ids[entry_id] = str(rel)

            # Tags check
            for tag in data.get('tags') or []:
                if tag not in valid_tags:
                    errors.append(f"unknown tag '{tag}'")
            for defn in data.get('definitions') or []:
                if isinstance(defn, dict):
                    for tag in defn.get('tags') or []:
                        if tag not in valid_tags:
                            errors.append(f"unknown definition tag '{tag}'")

            # Schema check
            try:
                jsonschema.validate(instance=data, schema=schema)
            except jsonschema.ValidationError as e:
                path = " -> ".join(str(p) for p in e.absolute_path) or "(root)"
                errors.append(f"schema {path}: {e.message}")

            if errors:
                has_errors = True
                print(f"❌ {rel}:1")
                for err in errors:
                    print(f"  • {err}")

    print()
    if has_errors:
        print("❌ Validation failed")
        sys.exit(1)
    print("✔️ Valid")


if __name__ == '__main__':
    main()
