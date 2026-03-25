# Kaitag Dictionary

Source repository for a bilingual (English/Russian) dictionary of Kaitag, a Northeast Caucasian language spoken in Dagestan.

Browse the dictionary at [urssivar.com/language/dictionary](https://urssivar.com/language/dictionary).

## Status & Roadmap

**v1.1 (in progress)**: enriching entries with examples and cross-references, normalizing structure, improving tooling.

- Letter **а**: complete (~175 entries)
- Remaining letters: in progress — priority is capturing meanings and examples while speaker access is available

**Future**: proper dialect variant entries; tag taxonomy improvements; analysis and stats scripts; lexicographic structure review after consulting reference literature

## Entry Format

Lexemes live in `lexicon/[letter]/`, one YAML file per entry named after its headword (e.g. `абаба.yaml`). Homonyms: `аккор.yaml`, `аккор-2.yaml`. Fields in four blocks separated by blank lines:

```yaml
# Block 1: Identity
id: YkZtiqCYGrbTzESn1sZW # required; generate with command
headword: абаба # required; default citation form
ipa: abaˈba
tags: [n]
forms:
  - text: абабне
    gloss: pl

# Block 2: Definitions
definitions: # required; one or more senses
  - translation:
      en: maternal grandmother
      ru: бабушка по матери
    tags: [kinship]
    examples:
      - text: Дами дила абаба риччихид.
        translation:
          en: I love my grandmother.
          ru: Я люблю мою бабушку.

# Block 3: About
etymology:
  en: Reduplication of *аба* "mother" (cf. *аттаба* "paternal grandmother").
  ru: Редупликация *аба* "мама" (ср. *аттаба* "бабушка по отцу").

# Block 4: Links
variants: [авба, бавба]
derived_from: [уба]
see_also: [аттаба]
```

Reference tables in `meta/` include the tag taxonomy (`tags.yaml`) and alphabet with IPA mappings (`alphabet.yaml`).

See [EDITORIAL_GUIDELINES.md](EDITORIAL_GUIDELINES.md) for all authoring rules and [ORTHOGRAPHY.md](ORTHOGRAPHY.md) for spelling conventions.

## Setup

Install the [YAML by Red Hat](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) VSCode extension — the schema at `.vscode/lexeme-schema.json` provides autocomplete and validation for all `lexicon/**/*.yaml` files.

[Claude Code](https://claude.ai/claude-code) with the `lexeme-polish` skill can assist with entry review, but all review decisions remain with the author.

Python scripts in `scripts/` handle validation and export, driven by `d.py` at the project root.

```bash
python d.py new <headword>      # create a new entry file
python d.py validate [а б]      # validate entries
python d.py export              # create files to export/
```

## License

**Content** under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), **Code** under [MIT](https://opensource.org/licenses/MIT).

When using the dictionary data, cite as:

> Magomedov, M., & Gasanova, U. (2026). Kaitag Dictionary [Data set].
> Licensed under CC BY-SA 4.0. <https://github.com/urssivar/dictionary>
