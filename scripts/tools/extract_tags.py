#!/usr/bin/env python3
import yaml
from pathlib import Path

lexicon_dir = Path(__file__).parent.parent.parent / 'lexicon'

all_tags = set()
word_level_tags = set()
definition_level_tags = set()

for yaml_file in lexicon_dir.rglob("*.yaml"):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        if not data or not isinstance(data, dict):
            continue
        for tag in data.get('tags') or []:
            all_tags.add(tag)
            word_level_tags.add(tag)
        for defn in data.get('definitions') or []:
            for tag in defn.get('tags') or []:
                all_tags.add(tag)
                definition_level_tags.add(tag)
    except Exception as e:
        print(f"Error processing {yaml_file}: {e}")

sep = "=" * 60
print(f"{sep}\nALL UNIQUE TAGS\n{sep}")
for tag in sorted(all_tags):
    print(f"  {tag}")
print(f"\nTotal: {len(all_tags)}")

print(f"\n{sep}\nWORD-LEVEL TAGS\n{sep}")
for tag in sorted(word_level_tags):
    print(f"  {tag}")
print(f"\nTotal: {len(word_level_tags)}")

print(f"\n{sep}\nDEFINITION-LEVEL TAGS\n{sep}")
for tag in sorted(definition_level_tags):
    print(f"  {tag}")
print(f"\nTotal: {len(definition_level_tags)}")
