# Kaitag Dictionary

Source repository for a bilingual (English/Russian) dictionary of Kaitag, a Northeast Caucasian language spoken in Dagestan.

Browse the dictionary at [urssivar.com/language/dictionary](https://urssivar.com/language/dictionary).

## Entry Format

Lexemes live in `entries/[letter]/`, one YAML file per entry named after its headword (e.g. `абаба.yaml`), with spaces replaced by underscores (e.g. `алав_биркара.yaml`). Homonyms: `аккор.yaml`, `аккор-2.yaml`. Four blocks separated by blank lines: Identity, Definitions, About, Links.

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

**v1.1 (in progress):** Open-source YAML repository with editorial guidelines and tooling. Enriching entries with cross-references, usage examples, semantic tags, aliases, etymologies, and notes.

- Letter **а**: complete (~175 entries)
- Remaining letters: in progress — priority is clarifying meanings and capturing examples

**v1.2:** orthographic standard — word division, punctuation, capitalization, loanword handling.

**[Future](https://github.com/urssivar/dictionary/issues/2):** dialect variant entries; tag taxonomy; corpus stats; lexicographic review against reference literature; morphological annotation and paradigm generation

**[v1.0 (May 2025)](https://github.com/urssivar/dictionary/releases/tag/v1.0):** Import of JSON source from Bazur dictionary, converted to YAML files. Co-authored with U. Gasanova, based on her dissertation wordlist appendix. Output features: accented headwords, grammatical forms, POS tags, dialectal variants.

## License

**Content** under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), **Code** under [MIT](https://opensource.org/licenses/MIT).

When citing a specific release, see its [release notes](https://github.com/urssivar/dictionary/releases) for the versioned citation. To cite the current state:

> Magomedov, M. (2026). Kaitag Dictionary.
> Licensed under CC BY-SA 4.0. <https://github.com/urssivar/dictionary>
