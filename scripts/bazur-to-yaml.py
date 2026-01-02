#!/usr/bin/env python3
"""Convert Kaitag dictionary from JSON to YAML format."""

import json
import yaml
import sys
from pathlib import Path
from collections import defaultdict


class InlineListDumper(yaml.SafeDumper):
    """YAML dumper: inline lists, block dicts."""

    def increase_indent(self, flow=False, indentless=False):
        """Override to control indentation."""
        return super().increase_indent(flow, False)


def represent_list(dumper, data):
    """Simple lists (scalars only) in flow style, complex lists in block style."""
    # Use flow style only for lists of scalars (like tags)
    is_simple = all(isinstance(item, (str, int, float, bool, type(None))) for item in data)
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=is_simple)


def represent_dict(dumper, data):
    """Dicts always in block style, never inline."""
    return dumper.represent_mapping('tag:yaml.org,2002:map', data, flow_style=False)


def represent_str(dumper, data):
    """Use literal style for multiline strings."""
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


InlineListDumper.add_representer(list, represent_list)
InlineListDumper.add_representer(dict, represent_dict)
InlineListDumper.add_representer(str, represent_str)


def load_alphabet():
    """Load Kaitag alphabet from data file."""
    alphabet_file = Path(__file__).parent.parent / 'data' / 'alphabet.yaml'
    with open(alphabet_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    alphabet = data['alphabet']
    return sorted(alphabet, key=len, reverse=True)


def get_first_letter(word, alphabet_tokens):
    """Get first letter, respecting digraphs."""
    word = word.lower()
    for letter in alphabet_tokens:
        if word.startswith(letter):
            return letter
    print(f'Warning: unknown first letter in "{word}"')
    return word[0]


# Tag conversions
GRAMMAR_TAGS = {
    'noun': 'n', 'verb': 'v', 'verbal': 'nmlz', 'nominal': 'n.nmlz',
    'adjective': 'adj', 'adverb': 'adv', 'pronoun': 'pro', 'numeral': 'num',
    'conjunction': 'conj', 'interjection': 'intj', 'postposition': 'post',
    'preposition': 'prep', 'determiner': 'det', 'particle': 'ptcl',
    'copula': 'cop', 'clitic': 'clt', 'transitive': 'tr',
    'intransitive': 'intr', 'labile': 'lbl', 'phrasal': 'phr',
    'class': 'cls', 'plural': 'pl',
}

TYPO_FIXES = {
    'intrasitive': 'intr', 'intranstive': 'intr', 'instransitive': 'intr',
    'trasitive': 'tr', 'lablile': 'lbl', 'varbal': 'nmlz',
    'phrasl': 'phr', 'phrasak': 'phr', 'pharasal': 'phr', 'phrase': 'phr',
    'arabuc': 'arabic', 'conjucntion': 'conj', 'animals': 'animal',
    'cloting': 'clothing', 'clothes': 'clothing', 'profesion': 'profession',
    'agruculture': 'agriculture', 'technology': 'tech', 'linguistic': 'linguistics',
}


def convert_tags(tags):
    """Convert tags to leipzig codes and fix typos."""
    result = []
    for tag in tags:
        tag = tag.strip()
        if not tag:
            continue
        tag = TYPO_FIXES.get(tag, tag)
        result.append(GRAMMAR_TAGS.get(tag, tag))
    return result


def parse_note(text):
    """Parse note into bilingual dict. Lines with 'Ru:' → ru, others → en."""
    if not text:
        return None

    en_lines, ru_lines = [], []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('Ru: ') or line.startswith('Ru:'):
            ru_lines.append(line[4:] if line.startswith('Ru: ') else line[3:])
        else:
            en_lines.append(line)

    result = {}
    if en_lines:
        result['en'] = '\n'.join(en_lines)
    if ru_lines:
        result['ru'] = '\n'.join(ru_lines)
    return result or None


def extract_etymology(text):
    """Extract etymology from note. Returns (etymology, remaining_note)."""
    if not text or '####' not in text:
        return None, parse_note(text)

    etymology, other_notes = {}, []
    section, etym_en, etym_ru = None, [], []

    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('#### Origin'):
            section = 'origin'
        elif line.startswith('####'):
            section = 'other'
        elif section == 'origin' and line:
            if line.startswith('Ru: ') or line.startswith('Ru:'):
                etym_ru.append(line[4:] if line.startswith('Ru: ') else line[3:])
            else:
                etym_en.append(line)
        elif section == 'other' and line:
            other_notes.append(line)

    if etym_en:
        etymology['en'] = '\n'.join(etym_en)
    if etym_ru:
        etymology['ru'] = '\n'.join(etym_ru)

    remaining = parse_note('\n'.join(other_notes)) if other_notes else None
    return (etymology or None), remaining


def convert_entry(entry):
    """Convert JSON entry to YAML structure."""
    result = {'id': entry['id'], 'headword': entry['headword']}

    if entry.get('ipa'):
        result['ipa'] = entry['ipa']
    if entry.get('tags'):
        result['tags'] = convert_tags(entry['tags'])

    # Extract etymology from word-level note
    if entry.get('note'):
        etymology, note = extract_etymology(entry['note'])
        if etymology:
            result['etymology'] = etymology
        if note:
            result['note'] = note

    # Forms
    if entry.get('forms'):
        result['forms'] = []
        for form in entry['forms']:
            form_obj = {'text': form['text']}
            if form.get('meaning'):
                form_obj['gloss'] = form['meaning']
            result['forms'].append(form_obj)

    # Definitions
    if entry.get('definitions'):
        result['definitions'] = []
        for defn in entry['definitions']:
            def_obj = {}

            # Translation
            translation = {}
            if defn.get('translation'):
                translation['en'] = defn['translation']

            # Parse note for Ru: translations
            if defn.get('note'):
                parsed = parse_note(defn['note'])
                if parsed:
                    if 'ru' in parsed:
                        translation['ru'] = parsed['ru']
                    if 'en' in parsed:
                        def_obj['note'] = {'en': parsed['en']}

            if translation:
                def_obj['translation'] = translation
            if defn.get('tags'):
                def_obj['tags'] = convert_tags(defn['tags'])

            # Aliases
            if defn.get('aliases'):
                aliases = [a for a in defn['aliases'] if a.strip()]
                if aliases:
                    def_obj['aliases'] = {'en': aliases}

            # Examples
            if defn.get('examples'):
                def_obj['examples'] = []
                for ex in defn['examples']:
                    ex_obj = {'text': ex['text']}
                    if ex.get('meaning'):
                        ex_obj['translation'] = {'en': ex['meaning']}
                    def_obj['examples'].append(ex_obj)

            result['definitions'].append(def_obj)

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 json-to-yaml.py input.json")
        sys.exit(1)

    alphabet_tokens = load_alphabet()

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} entries")

    # Track homonyms
    headword_counts = defaultdict(int)
    for entry in data:
        headword_counts[entry['headword']] += 1

    headword_index = defaultdict(int)
    lexicon_dir = Path('lexicon')
    lexicon_dir.mkdir(exist_ok=True)

    # Convert entries
    for entry in data:
        converted = convert_entry(entry)
        headword = converted['headword']
        first_letter = get_first_letter(headword, alphabet_tokens)

        letter_dir = lexicon_dir / first_letter
        letter_dir.mkdir(exist_ok=True)

        # Handle homonyms
        headword_index[headword] += 1
        if headword_counts[headword] > 1 and headword_index[headword] > 1:
            filename = f"{headword}-{headword_index[headword]}.yaml"
        else:
            filename = f"{headword}.yaml"

        with open(letter_dir / filename, 'w', encoding='utf-8') as f:
            yaml.dump(converted, f,
                     Dumper=InlineListDumper,
                     allow_unicode=True,
                     default_flow_style=None,
                     sort_keys=False,
                     width=float('inf'))

    print(f"Converted {len(data)} entries to {lexicon_dir}/")
    print(f"Found {sum(1 for c in headword_counts.values() if c > 1)} homonym sets")

    # Stats
    letter_counts = {d.name: len(list(d.glob('*.yaml')))
                    for d in lexicon_dir.iterdir() if d.is_dir()}
    print("\nEntries per letter:")
    for letter in sorted(letter_counts.keys()):
        print(f"  {letter}: {letter_counts[letter]}")


if __name__ == '__main__':
    main()
