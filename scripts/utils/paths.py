#!/usr/bin/env python3
from pathlib import Path


def _find_root() -> Path:
    for parent in Path(__file__).parents:
        if (parent / 'd.py').exists():
            return parent
    raise RuntimeError("Could not find project root (no d.py found)")


ROOT = _find_root()
