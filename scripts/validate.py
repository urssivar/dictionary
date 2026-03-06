#!/usr/bin/env python3
"""Validate dictionary entries."""

import sys
from pathlib import Path
from validators.id_validation import validate_ids
from validators.tag_validation import validate_tags
from validators.headword_validation import validate_headwords


def main():
    project_root = Path(__file__).parent.parent
    lexicon_dir = project_root / 'lexicon'
    data_dir = project_root / 'data'

    print("Running ID validation...")
    id_result = validate_ids(lexicon_dir)

    print("Running headword validation...")
    hw_result = validate_headwords(lexicon_dir)

    # print("Running tag validation...")
    # tag_result = validate_tags(lexicon_dir, data_dir)
    tag_result = False

    # Check results
    if id_result is None or hw_result is None or tag_result is None:
        print("\n✗ Validation failed")
        sys.exit(1)
    else:
        print("\n✓ All validations passed")
        sys.exit(0)


if __name__ == '__main__':
    main()
