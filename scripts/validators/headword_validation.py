#!/usr/bin/env python3
"""Validate headword–filename–folder consistency."""

import re
import yaml
from pathlib import Path
from utils.loaders import load_alphabet


def _folder_for_headword(headword: str, alphabet_tokens: list[str]) -> str | None:
    """Return the grapheme (folder name) that headword starts with, or None."""
    for token in alphabet_tokens:
        if token in ('-', ' '):
            continue
        if headword.startswith(token):
            return token
    return None


def validate_headwords(lexicon_dir: Path) -> bool | None:
    """Check headword–filename match and correct letter folder.

    Returns None on failure, True on success.
    """
    _, alphabet_tokens, _ = load_alphabet()

    has_errors = False

    for yaml_file in sorted(lexicon_dir.rglob("*.yaml")):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            has_errors = True
            print(f"ERROR: YAML parse error in {yaml_file.relative_to(lexicon_dir.parent)}: {e}")
            continue

        if not data:
            continue

        folder = yaml_file.parent.name
        stem = yaml_file.stem  # e.g. "аккор" or "аккор-2"

        # Strip homonym numeric suffix: "аккор-2" → "аккор"
        headword_from_filename = re.sub(r'-\d+$', '', stem).lower()

        # Rule 1: headword must match filename (sans suffix)
        headword = data.get('headword')
        if headword is None:
            print(f"ERROR: missing 'headword'\n  {yaml_file.relative_to(lexicon_dir.parent)}:1")
            has_errors = True
        elif headword.lower() != headword_from_filename:
            print(
                f"ERROR: headword/filename mismatch: "
                f"headword={headword!r}, filename implies {headword_from_filename!r}\n  {yaml_file.relative_to(lexicon_dir.parent)}:1"
            )
            has_errors = True

        # Rule 2: file must be in the correct letter folder
        if headword:
            expected_folder = _folder_for_headword(headword.lower(), alphabet_tokens)
            if expected_folder is None:
                print(f"ERROR: cannot determine letter folder for headword {headword!r}\n  {yaml_file.relative_to(lexicon_dir.parent)}:1")
                has_errors = True
            elif folder != expected_folder:
                print(
                    f"ERROR: wrong folder: headword {headword!r} belongs in '{expected_folder}/', found in '{folder}/'\n  {yaml_file.relative_to(lexicon_dir.parent)}:1"
                )
                has_errors = True

    if has_errors:
        return None
    return True
