#!/usr/bin/env python3

import re
import yaml
from pathlib import Path
from utils.loaders import load_alphabet


def _folder_for_headword(headword: str, alphabet_tokens: list[str]) -> str | None:
    for token in alphabet_tokens:
        if token in ('-', ' '):
            continue
        if headword.startswith(token):
            return token
    return None


def validate_headwords(lexicon_dir: Path) -> bool:
    _, alphabet_tokens, _ = load_alphabet()

    has_errors = False

    for yaml_file in sorted(lexicon_dir.rglob("*.yaml")):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            has_errors = True
            print(f"❌ YAML parse error: {e}\n  {yaml_file.relative_to(lexicon_dir.parent)}:1")
            continue

        if not data:
            continue

        folder = yaml_file.parent.name
        headword_from_filename = re.sub(r'-\d+$', '', yaml_file.stem).lower()
        headword = data.get('headword')
        if headword is None:
            print(f"❌ missing 'headword'\n  {yaml_file.relative_to(lexicon_dir.parent)}:1")
            has_errors = True
        elif headword.lower() != headword_from_filename:
            print(
                f"❌ headword/filename mismatch: "
                f"headword={headword!r}, filename implies {headword_from_filename!r}\n  {yaml_file.relative_to(lexicon_dir.parent)}:1"
            )
            has_errors = True

        if headword:
            expected_folder = _folder_for_headword(headword.lower(), alphabet_tokens)
            if expected_folder is None:
                print(f"❌ cannot determine letter folder for headword {headword!r}\n  {yaml_file.relative_to(lexicon_dir.parent)}:1")
                has_errors = True
            elif folder != expected_folder:
                print(
                    f"❌ wrong folder: headword {headword!r} belongs in '{expected_folder}/', found in '{folder}/'\n  {yaml_file.relative_to(lexicon_dir.parent)}:1"
                )
                has_errors = True

    if has_errors:
        return False
    return True
