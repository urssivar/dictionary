#!/usr/bin/env python3
"""Validate dictionary entries."""

import sys
from pathlib import Path
from validators.id_collision import validate_id_collisions


def main():
    lexicon_dir = Path(__file__).parent.parent / 'lexicon'

    print("Running ID collision validation...")

    result = validate_id_collisions(lexicon_dir)

    if result is None:
        print("\n✗ Validation failed")
        sys.exit(1)
    else:
        print("✓ No ID collisions found")
        sys.exit(0)


if __name__ == '__main__':
    main()
