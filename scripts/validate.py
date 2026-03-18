#!/usr/bin/env python3
"""Validate dictionary entries: IDs, headwords, and tags."""

import sys
from utils.paths import ROOT
from validators.id_validation import validate_ids
from validators.headword_validation import validate_headwords
from validators.tag_validation import validate_tags


def main():
    lexicon_dir = ROOT / 'lexicon'
    data_dir = ROOT / 'data'

    id_result = validate_ids(lexicon_dir)
    hw_result = validate_headwords(lexicon_dir)
    tag_result = validate_tags(lexicon_dir, data_dir)

    if not id_result or not hw_result or not tag_result:
        print("\n❌ Validation failed")
        sys.exit(1)
    print("\n✔️ Valid")


if __name__ == '__main__':
    main()
