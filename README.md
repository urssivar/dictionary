# Kaitag Dictionary

Source repository for a bilingual (English/Russian) dictionary of the Kaitag language, a Northeast Caucasian language spoken in Dagestan.

## Project Structure

```
lexicon/[letter]/              — one YAML file per lexeme, organized by first letter
data/alphabet.yaml             — Kaitag alphabet with digraphs and IPA mappings
data/tags.yaml                 — complete tag taxonomy (grammar, etymology, register, semantic)
data/lects.yaml                — dialect inventory
scripts/                       — export and validation scripts
.vscode/lexeme-schema.json     — JSON schema for lexeme files (powers VSCode autocomplete)
EDITORIAL_GUIDELINES.md            — editorial rules and conventions
```

## Entry Format

Each entry is a standalone YAML file. Fields are grouped in three blocks separated by blank lines:

```yaml
# Block 1: Identity
id: SaZFtrg5rkjmNmX7pMDn
headword: абиккан
ipa: abiˈkːan
tags: [n, vb]
forms:
  - text: абикканил
    gloss: obl
  - text: адикканте
    gloss: pl

# Block 2: Content
definitions:
  - translation:
      en: disappointment
      ru: огорчение
    tags: [feeling]
    aliases:
      en: [letdown, disillusionment]
      ru: [разочарование, расстройство]
    examples:
      - text: Ил ьелей абиккан баривде.
        translation:
          en: You disappointed him.
          ru: Ты огорчил его.

# Block 3: References
etymology:
  en: Negative present participle of *биккара* "to want".
  ru: Отрицательное настоящее причастие от *биккара* "хотеть".
derived_from: [биккара]
see_also: [биккан]
```

### Required Fields

- `id` — unique nanoid (generate with `python3 scripts/tools/generate_id.py`)
- `headword` — citation form (abs sg for nouns, ipfv inf for verbs)
- `definitions` — at least one definition

### Bilingual Fields

`translation`, `aliases`, `note`, `etymology`, and `examples.translation` all take `{en:, ru:}` objects.

### Tag System

All valid tags are in `data/tags.yaml`. Tags fall into four categories:

- **Grammar** (entry-level): `n`, `v`, `adj`, `adv`, `tr`, `ntr`, `cls`, `pl`, `vb`, etc.
- **Etymology** (entry-level): `loan`, `arabic`, `turkic`, `iranian`, `russian`
- **Register/semantic** (definition-level): `pejorative`, `child`, `kinship`, `animal`, `food`, `tool`, `body`, etc.

### Forms

Only list forms that differ from the headword. The headword is the default citation form (abs sg for nouns, ipfv for verbs) — don't repeat it.

For compound verbs, list only the verbal part (the nominal part never changes).

Syncretic forms use comma-separated glosses: `gloss: obl, loc`.

### Variants

Plain string array. For variants with their own paradigm, slash-separate the forms within one string. Use `~` for forms identical to the headword's corresponding form:

```yaml
variants: [тӏя / тӏял- / тӏяме, тӏяь / тӏяьу / тӏяьри]
variants: [~ / барара / барив]
```

### File Naming

- Headword = filename (e.g. `абиккан.yaml`)
- Homonyms: `аккор.yaml`, `аккор-2.yaml`, `аккор-3.yaml`
- File must be in the folder matching its first letter/digraph

## Scripts

Run from the `scripts/` directory with the virtualenv active:

```bash
cd scripts
source ../venv/bin/activate

python3 validate.py          # validate all entries (IDs, headwords, tags)
python3 export.py            # validate + build all export formats
python3 to_json_web.py       # build website JSON only
python3 to_csv.py            # build CSV only
```

Exports are written to `export/`.

## VSCode Setup

Install the **YAML by Red Hat** extension. The schema at `.vscode/lexeme-schema.json` is automatically applied to all `lexicon/**/*.yaml` files, providing autocomplete and validation.

## Status & Roadmap

- **Letter а**: complete (~175 entries), v1.1 conventions established
- **In progress**: remaining letters — priority is capturing meanings and examples while speaker access is available
- **Planned**: proper dialect variant entries (currently stored as plaintext in `variants`); semantic tags `health`, `language`, `behavior` when ready

## Contributing

See [`EDITORIAL_GUIDELINES.md`](EDITORIAL_GUIDELINES.md) for the full editorial guide covering translations, forms, tags, etymology, cross-references, and examples.

## License

**Content** under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), **Code** under [MIT](https://opensource.org/licenses/MIT).

When using the dictionary data, cite as:

```
Magomedov, M., & Gasanova, U. (2026). Kaitag Dictionary [Data set].
Licensed under CC BY-SA 4.0. https://github.com/urssivar/dictionary
```
