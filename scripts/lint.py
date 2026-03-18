#!/usr/bin/env python3

import json
import sys
import yaml
import argparse
from pathlib import Path

import jsonschema
from utils.paths import ROOT


def validate_schema(letter_dir: Path, schema: dict, root: Path) -> bool:
    has_errors = False
    for yaml_file in sorted(letter_dir.rglob("*.yaml")):
        try:
            with open(yaml_file, encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            has_errors = True
            print(f"❌ YAML parse error: {e}\n  {yaml_file.relative_to(root)}:1")
            continue
        if not data:
            continue
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.ValidationError as e:
            has_errors = True
            path = " -> ".join(str(p) for p in e.absolute_path) or "(root)"
            print(f"❌ schema: {path}: {e.message}\n  {yaml_file.relative_to(root)}:1")
    return not has_errors


def main():
    parser = argparse.ArgumentParser(description="Lint dictionary entries against JSON Schema.")
    parser.add_argument("letters", nargs="*", metavar="LETTER",
                        help="Letter folder(s) to lint (default: all)")
    args = parser.parse_args()

    lexicon_dir = ROOT / 'lexicon'
    schema_path = ROOT / '.vscode' / 'lexeme-schema.json'

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
        dirs = [d for d in sorted(lexicon_dir.iterdir()) if d.is_dir()]

    failed = any(not validate_schema(d, schema, ROOT) for d in dirs)

    if failed:
        print("\n❌ Lint failed")
        sys.exit(1)
    print("\n✔️ Valid")


if __name__ == '__main__':
    main()
