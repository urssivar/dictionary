#!/usr/bin/env python3
import os
import yaml
from pathlib import Path

# Set to store all unique tags
all_tags = set()
word_level_tags = set()
definition_level_tags = set()

# Walk through the lexicon directory
lexicon_dir = Path("lexicon")

for yaml_file in lexicon_dir.rglob("*.yaml"):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

            # Extract word-level tags
            if data and isinstance(data, dict):
                if 'tags' in data and data['tags']:
                    for tag in data['tags']:
                        all_tags.add(tag)
                        word_level_tags.add(tag)

                # Extract definition-level tags
                if 'definitions' in data and isinstance(data['definitions'], list):
                    for definition in data['definitions']:
                        if isinstance(definition, dict) and 'tags' in definition and definition['tags']:
                            for tag in definition['tags']:
                                all_tags.add(tag)
                                definition_level_tags.add(tag)
    except Exception as e:
        print(f"Error processing {yaml_file}: {e}")

# Print results
print("=" * 60)
print("ALL UNIQUE TAGS")
print("=" * 60)
for tag in sorted(all_tags):
    print(f"  {tag}")

print(f"\nTotal unique tags: {len(all_tags)}")

print("\n" + "=" * 60)
print("WORD-LEVEL TAGS")
print("=" * 60)
for tag in sorted(word_level_tags):
    print(f"  {tag}")

print(f"\nTotal word-level tags: {len(word_level_tags)}")

print("\n" + "=" * 60)
print("DEFINITION-LEVEL TAGS")
print("=" * 60)
for tag in sorted(definition_level_tags):
    print(f"  {tag}")

print(f"\nTotal definition-level tags: {len(definition_level_tags)}")
