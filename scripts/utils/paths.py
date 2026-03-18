#!/usr/bin/env python3
from pathlib import Path


def _find_root() -> Path:
    for parent in Path(__file__).parents:
        if (parent / 'Makefile').exists():
            return parent
    raise RuntimeError("Could not find project root (no Makefile found)")


ROOT = _find_root()
