#!/usr/bin/env python3
"""Entry conversion helper utilities."""


def extract_yaml_variants(yaml_variants):
    """Extract variant text from YAML variants field.

    Args:
        yaml_variants: List of {text: "..."} objects from YAML

    Returns:
        List of variant strings
    """
    if not yaml_variants:
        return []

    return [v['text'] for v in yaml_variants if 'text' in v]


def map_tags(tags, tag_map):
    """Map tags to bilingual format, filter to grammar tags only.

    Returns array of {en:, ru:} objects.
    """
    if not tags:
        return []

    result = []
    for tag in tags:
        if tag in tag_map:
            result.append({
                'en': tag_map[tag]['en'],
                'ru': tag_map[tag]['ru']
            })

    return result


def simplify_forms(forms, headword, tags):
    """Extract and process forms with special handling for compound verbs and oblique stems."""
    if not forms:
        return []

    # Check if this is a compound verb (verb tag + space in headword)
    is_compound_verb = 'v' in tags and ' ' in headword

    result = []
    for form in forms:
        text = form.get('text', '')
        if not text or text == headword:
            continue

        # Compound verb: collapse first part to tilde
        if is_compound_verb:
            text = text.split()[-1]

        # Oblique stem: append dash
        if form.get('gloss') == 'obl':
            text += '-'

        result.append(text)

    return result
