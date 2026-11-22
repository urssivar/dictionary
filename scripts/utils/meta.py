#!/usr/bin/env python3
"""Cached access to meta/*.yaml — the single source of truth for alphabet and tags.

Loaders are lru_cached: the YAML is read once per process, and any helper can
call them without threading config through arguments. Tests can reset with
load_alphabet.cache_clear() / load_tags.cache_clear().
"""
from functools import lru_cache

import yaml

from utils.paths import ROOT


@lru_cache(maxsize=1)
def load_alphabet():
    """Raw meta/alphabet.yaml: {'alphabet': {grapheme: {'ipa': ..., 'type': ...}}}."""
    with open(ROOT / 'meta' / 'alphabet.yaml', encoding='utf-8') as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def letters():
    """Graphemes in alphabet order (the letter folder names)."""
    return list(load_alphabet()['alphabet'].keys())


@lru_cache(maxsize=1)
def load_tags():
    """Raw meta/tags.yaml taxonomy."""
    with open(ROOT / 'meta' / 'tags.yaml', encoding='utf-8') as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def valid_tags():
    taxonomy = load_tags()
    return {
        k
        for cat in taxonomy.values()
        if isinstance(cat, dict)
        for k in cat
    }


@lru_cache(maxsize=1)
def grammar_tag_map():
    exportable = {
        'n', 'v', 'adj', 'adv', 'conj', 'prep', 'post',
        'intj', 'pro', 'num', 'cop', 'ptcl', 'det', 'cls', 'pl', 'aff'
    }
    return {
        short: {'en': tag['en'], 'ru': tag['ru']}
        for short, tag in load_tags()['grammar'].items()
        if short in exportable
    }
