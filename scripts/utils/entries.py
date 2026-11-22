#!/usr/bin/env python3
"""Entry discovery: the single walker over entries/, the '-N' id convention,
entry loading, and headword cross-reference resolution."""
import re

import yaml

from utils.paths import ROOT
from utils.meta import letters
from utils.text import first_letter


def clean_id(name):
    """Filename stem as a ref id: 'давкк-2' → 'давкк', underscores → spaces."""
    return re.sub(r'-\d+$', '', name).replace('_', ' ')


def iter_entry_files():
    """Yield (letter, path) for every entry file, in letter then name order."""
    for letter in letters():
        letter_dir = ROOT / 'entries' / letter
        if letter_dir.is_dir():
            for path in sorted(letter_dir.glob('*.yaml')):
                yield letter, path


def load_entries():
    """Entries grouped by letter folder: {letter: [entry dicts with 'id']},
    plus (total, skipped). Unreadable files are reported and skipped."""
    entries_by_letter = {letter: [] for letter in letters()}
    total_entries = 0
    skipped_entries = 0

    for letter, path in iter_entry_files():
        try:
            with open(path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
            data['id'] = path.stem
            entries_by_letter[letter].append(data)
            total_entries += 1
        except Exception as e:
            skipped_entries += 1
            print(f"{path.relative_to(ROOT)}\n  • {e}")

    return entries_by_letter, total_entries, skipped_entries


def resolve_headword_ref(ref):
    """Path of the referenced entry file; True for '*' wildcards; None if missing."""
    if ref.startswith('*'):
        return True
    path = ROOT / 'entries' / first_letter(ref) / f"{ref}.yaml"
    return path if path.exists() else None
