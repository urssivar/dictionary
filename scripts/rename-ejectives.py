#!/usr/bin/env python3
"""Rename files and directories containing soft-sign ejective digraphs with palochka."""

import os
import re

REPLACEMENTS = [
    ("пь", "пӏ"),
    ("ть", "тӏ"),
    ("ць", "цӏ"),
    ("чь", "чӏ"),
    ("кь", "кӏ"),
    ("ҡь", "ҡӏ"),
]


def apply_replacements(name):
    for src, dst in REPLACEMENTS:
        name = name.replace(src, dst)
    return name


def needs_rename(name):
    return any(src in name for src, _ in REPLACEMENTS)


def rename_tree(root):
    # Walk bottom-up so we rename children before parents
    renames = []
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for filename in filenames:
            if needs_rename(filename):
                old = os.path.join(dirpath, filename)
                new = os.path.join(dirpath, apply_replacements(filename))
                renames.append((old, new))
        basename = os.path.basename(dirpath)
        if needs_rename(basename):
            new_basename = apply_replacements(basename)
            new_dirpath = os.path.join(os.path.dirname(dirpath), new_basename)
            renames.append((dirpath, new_dirpath))

    for old, new in renames:
        print(f"  {os.path.relpath(old)} -> {os.path.relpath(new)}")
        os.rename(old, new)

    return len(renames)


def main():
    lexicon_dir = os.path.join(os.path.dirname(__file__), '..', 'lexicon')
    count = rename_tree(lexicon_dir)
    print(f"\nDone. {count} items renamed.")


if __name__ == '__main__':
    main()
