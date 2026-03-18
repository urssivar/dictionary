#!/usr/bin/env python3
import yaml
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.paths import ROOT


def main():
    lexicon_dir = ROOT / 'lexicon'

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
            print(f"❌ {yaml_file}: {e}")

    def section(title, tags):
        print(f"\n— {title} ({len(tags)}) —")
        for tag in sorted(tags):
            print(f"  {tag}")

    section("all", all_tags)
    section("word-level", word_level_tags)
    section("definition-level", definition_level_tags)


if __name__ == '__main__':
    main()
