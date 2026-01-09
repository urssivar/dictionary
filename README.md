# Kaitag Dictionary

Digital dictionary for the Kaitag language with 5,171 entries, exported from the Bazur dictionary app.

## Project Structure

```
├── data/              # Reference data
│   ├── alphabet.yaml  # Kaitag alphabet with digraphs
    └── bazur.json     # Source data from Bazur app
├── lexicon/           # Dictionary entries (one YAML file per entry)
│   ├── а/             # Organized by first letter
│   ├── б/
│   ├── кк/            # Digraphs get their own folders
│   └── ...
└── scripts/           # Conversion utilities
    └── bazur-to-yaml.py
```

## Quick Start

### Convert from Bazur JSON to YAML

```bash
python3 scripts/bazur-to-yaml.py data/bazur.json
```

This creates individual YAML files in `/lexicon/` organized by first letter.

### Entry Format

Each entry is a standalone YAML file:

```yaml
id: unique-id
headword: абиккан
ipa: abiˈkːan
tags: [n, nmlz]
etymology:
  en: Neg. obl. of *биккара* "to want"
forms:
  - text: абиккан
    gloss: abs
  - text: абикканил
    gloss: obl
definitions:
  - translation:
      en: disappointment
      ru: огорчение
    examples:
      - text: дами абиккан агур
        translation:
          en: i got disappointed
```

## Data Structure

### Required Fields
- `id` - Unique identifier
- `headword` - The Kaitag word
- `definitions` - At least one definition

### Optional Fields
- `ipa` - IPA pronunciation
- `tags` - Grammar and semantic tags
- `etymology` - Word origin (bilingual)
- `note` - Usage notes (bilingual)
- `forms` - Inflectional paradigm
- `variants` - Dialectal variants
- `derived_from` - Source words
- `see_also` - Cross-references

### Bilingual Fields

Most text fields support optional `en` and `ru` keys:

```yaml
translation:
  en: English translation
  ru: Russian translation
```

### Tag System

**Grammar tags** use Leipzig glossing codes:
- `n` (noun), `v` (verb), `adj` (adjective), `adv` (adverb)
- `tr` (transitive), `intr` (intransitive)
- `phr` (phrasal), `cls` (class agreement)

**Semantic tags** use readable names:
- `loan`, `arabic`, `turkic`, `persian`, `russian`
- `kinship`, `emotion`, `animal`, `tool`, `food`

### File Organization

- **Homonyms**: First entry = `word.yaml`, subsequent = `word-2.yaml`, `word-3.yaml`
- **Digraphs**: Letters like `кк`, `чч`, `цц` get their own folders
- **No triple dashes**: Each file is a standalone YAML document

## YAML Formatting

- **Simple arrays**: Inline style → `tags: [n, v]`
- **Complex arrays**: Block style with proper indentation
- **All objects**: Block style (never inline `{key: value}`)
- **Multiline strings**: Literal style `|`

## Editing Workflow

1. **Conversion**: Run `bazur-to-yaml.py` to generate initial YAML files
2. **Editing**: Manual refinement in VSCode with YAML validation
3. **Future**: Convert back to JSON for static website

### VSCode Setup

Install **YAML by Red Hat** extension for:
- Autocomplete
- Schema validation
- Hover documentation

## Alphabet

Kaitag uses 42 letters including digraphs (stored in `/data/alphabet.yaml`):

```
а б в г ғ д е ж з и й к кк кь ҡ ҡҡ ҡь л м н о п пп пь
р с т тт ть у х ҳ ц цц ць ч чч чь ш ъ ь я
```

## Future Work

- Tag normalization and lookup tables (`/data/tags.yaml`, `/data/glosses.yaml`)
- Stress marking script for publication
- YAML→JSON converter for static website
- Audio pronunciation files

## Published Dictionary

This repository contains the **source data** for editing and development.

For browsing and using the dictionary, visit:

### **[📖 Kaitag Dictionary at Urssivar.com](https://urssivar.com/language/dictionary/intro)**

The published dictionary includes:
- **Online browsing** - Search and explore all 5,171 entries
- **PDF download** - Printable offline version
- **Google Sheets** - Spreadsheet format for analysis
- **Grammar guide** - Phonetics, orthography, and grammatical reference
- **Additional tools** - Keyboards, text converter, video introduction

---

## Authors

**Magomed Magomedov** and **Uzlipat Gasanova**

## License

This project uses dual licensing:

- **Dictionary data** (`/lexicon/`, `/data/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - Free to use, including commercially, with attribution
- **Code** (`/scripts/`): [MIT License](https://opensource.org/licenses/MIT) - Use freely without restrictions

See [LICENSE](LICENSE) for full details.

### Attribution

When using the dictionary data, please cite as:

```
Magomedov M., Gasanova U. (2025). Kaitag Dictionary [Data set].
https://github.com/urssivar/dictionary
```
