# Kaitag Dictionary

Source repository for a bilingual (English/Russian) dictionary of Kaitag, a Northeast Caucasian language spoken in Dagestan.

Browse the dictionary at [urssivar.com/language/dictionary](https://urssivar.com/language/dictionary).

## Entry Format

Lexemes live in `entries/[letter]/`, one YAML file per entry named after its headword (e.g. `абаба.yaml`), with spaces replaced by underscores (e.g. `алав_биркара.yaml`). Homonyms: `аккор.yaml`, `аккор-2.yaml`. Fields in four blocks separated by blank lines:

```yaml
# Block 1: Identity
headword: абаба
ipa: abaˈba
tags: [n]
forms:
  - text: абабне
    gloss: pl

# Block 2: Definitions
definitions:
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
derived_from: [уба]
variants: [авба, бавба]
see_also: [аттаба]
```

Reference tables in `meta/` include the tag taxonomy (`tags.yaml`) and alphabet with IPA mappings (`alphabet.yaml`).

See [guidelines.md](guidelines.md) for all authoring rules and spelling conventions, and [urssivar/script](https://github.com/urssivar/script) for the underlying script and character system.

## Setup

Install the [YAML by Red Hat](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) VSCode extension — the schema at `.vscode/entry-schema.json` provides autocomplete and validation for all `entries/**/*.yaml` files.

[Claude Code](https://claude.ai/claude-code) with the `entry-polish` skill can assist with entry review, but all review decisions remain with the author.

Python scripts in `scripts/` handle validation and export, driven by `d.py` at the project root.

```bash
python d.py new <headword>      # create a new entry file
python d.py validate [а б]      # validate entries
python d.py export              # create files to export/
```

## Version History

**v1.1 (2026, in progress):** Open-source YAML repository with editorial guidelines and tooling. Enriching entries with cross-references, usage examples, semantic tags, aliases, etymologies, and notes. Migrated to [Kaitag script v1.2](https://github.com/urssivar/script). In collaboration with **Gasanov M. R.** from Kirki village.

- Letter **а**: complete (~175 entries)
- Remaining letters: in progress — priority is clarifying meanings and capturing examples

**[Future](https://github.com/urssivar/dictionary/issues/2):** orthographic standard, corpus stats, lexicographic review, morphological annotation and paradigm generation, and more.

**[v1.0 (May 2025)](https://github.com/urssivar/dictionary/releases/tag/v1.0):** Import of JSON source from Bazur dictionary, converted to YAML files. Output features: accented headwords, grammatical forms, POS tags, dialectal variants. In collaboration with prof. **Gasanova U. U.**, based on her dissertation's Shilyagi village wordlist (2012). Additional references: **Temirbulatova S. M.** (2004, 2008, 2021), **Gabibova K. M.** (2009).

## License

**Content** under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), **Code** under [MIT](https://opensource.org/licenses/MIT).

When citing a specific release, see its [release notes](https://github.com/urssivar/dictionary/releases) for the versioned citation. To cite the current state:

> Magomedov, M. (2026). Kaitag Dictionary. Licensed under CC BY-SA 4.0. <https://github.com/urssivar/dictionary>
