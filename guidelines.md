# Kaitag Dictionary Guidelines

## Scope

**Deverbal adjectives** — Kaitag preterites regularly function as adjectives (*бӕрӏив* "cold" from *бурӏара* "to cool"). Add as a separate entry with `vb` tag and `derived_from` when frequent or lexicalized enough.

**Skip** lexically transparent productive patterns: causatives (*X барара* "to make X"), inchoatives (*X бирһора* "to become X"), regular adverbs with *-ле*, etc. These are grammar, not lexicon. Exception: include compound verbs with non-compositional meaning (e.g. *алав биркара* "to evade", not literally "to occur around").

## Structure

**Homonyms** — first entry is `word.yaml`, subsequent are `word-2.yaml`, `word-3.yaml`.

Four blocks separated by blank lines. Full schema at `.vscode/entry-schema.json`.

`validate.py` enforces: headword/filename match, correct letter folder, valid tags, and resolved cross-references. The schema enforces field types and required fields. The guidelines below cover judgment calls not caught by tooling.

```yaml
# Block 1: Identity
headword:
ipa:
tags:
forms:
  - text:
    gloss:

# Block 2: Definitions
definitions:
  - translation:
    tags:
    aliases:
    note:
    examples:
      - text:
        translation:

# Block 3: About
note:
etymology:

# Block 4: Links
variants:
derived_from:
see_also:
```

YAML conventions: simple arrays inline `[a, b]`; object arrays and all objects in block style.

## Fields

### `headword` & `forms`

For spelling conventions, see [Orthography](#orthography) below. For the alphabet and IPA mappings, see [meta/alphabet.yaml](meta/alphabet.yaml).

**Headword** is the default citation form:

- Nouns: absolutive singular
- Verbs: imperfective infinitive
- Copulas / person-agreeing words: 3rd person singular
- Words with class agreement: neutral *-б-* class marker; tag with `cls`

**Forms** — only list what differs from the headword. Omit `forms` entirely if nothing does. Use Leipzig abbreviations (<https://en.wikipedia.org/wiki/List_of_glossing_abbreviations>). Use `.` for portmanteau glosses (`1.sg.pst`), `,` for syncretism (`obl, loc` / `1, 2.pl`).

**Verbs** — list `pfv` and `pret` when they exist (some verbs lack one or both). For compound verbs, list only the verbal part (nominal part never inflects):

```yaml
headword: абиккул иҡара
forms:
  - text: аҡара
    gloss: pfv
  - text: аҡив
    gloss: pret
```

**Nouns** — list `pl`, `obl`, `loc` as applicable:

```yaml
headword: аҡ
forms:
  - text: аҡа
    gloss: obl
  - text: иҡре
    gloss: pl
```

### `tags`

Valid tags are in `meta/tags.yaml`. Grammar and etymology tags at entry level; semantic and register tags at definition level.

Required when applicable: `tr`/`ntr` for verbs, `cls` for class-agreeing words (any POS), `pl` for pluralia tantum nouns.

Use semantic tags sparingly — concrete content words only. Don't tag particles or abstract grammatical words. In particular:

- `culture` — concrete practices/objects, not abstract social nouns
- `disease` — conditions only, not substances or procedures
- `material` — raw substances, not objects made from them

### `translation` & `aliases`

**Translation:**

- Verbs: English infinitive with "to" (`to walk`); Russian imperfective infinitive (`ходить`)
- Nouns: singular unless plurale tantum
- Adjectives: English base form (`cold`); Russian masculine singular (`холодный`)
- Particles/function words: grammatical label with equivalents in parentheses:

```yaml
translation:
  en: affirmative particle (right?, isn't it?)
  ru: утвердительная частица (да же?, правда?)
```

**Aliases** — synonyms, hypernyms, and related terms for search discoverability. Match grammatical form of the translation. `en` and `ru` need not be parallel. Don't repeat the main translation or cross part-of-speech boundaries.

```yaml
definitions:
  - translation:
      en: entrance
      ru: вход
    tags: [structure]
    aliases:
      en: [entry, passage, doorway]
      ru: [проход]
```

### `note` & `examples`

**Note** — cultural/technical clarifications that don't fit in translation: kinship specifics, regional dishes, specialized terminology. One or two sentences. Full sentences end with period; nominal labels don't.

**Examples** — natural, idiomatic usage illustrating the specific definition. Include at least one for common or ambiguous words.

### `etymology`

Include for loanwords and non-obvious formations. Omit for transparent derivations (use `derived_from` instead) and for derived forms whose base loanword already has its own entry.

**Arabic/Persian:**

```yaml
etymology:
  en: From Arabic أَبَد (*ʔabad*) "eternity".
  ru: От арабского أَبَد (*ʔabad*) "вечность".
```

**Russian** — no transcription in English; no translation in Russian:

```yaml
etymology:
  en: From Russian *обои* "wallpaper" (pl.), reanalyzed as singular.
  ru: От русского *обои* (мн. ч.), переосмыслено как ед. ч.
```

**Turkic in Cyrillic** — no transcription; Cyrillic for Kumyk, Latin for Azerbaijani:

```yaml
etymology:
  en: From Kumyk *гьав* or Azerbaijani *ov* "hunt".
  ru: От кумыкского *гьав* или азербайджанского *ov* "охота".
```

**Chains:**

```yaml
etymology:
  en: From Kumyk *авара* "worry", ultimately from Persian آواره (*âvâre*) "vagabond".
  ru: От кумыкского *авара* "беспокойство", восходит к персидскому آواره (*âvâre*) "бродяга".
```

Formulae: `The negative of *verb* "gloss".` / `Negative present participle of *verb* "gloss".`

Formatting: *italics* for cited forms, "double quotes" for glosses, (parentheses) for supplementary notes.

### `variants`

Plain string array of dialectal/alternative forms. For variants with their own paradigm, slash-separate forms; use `~` for forms matching the headword. Include oblique dash `-` directly in string:

```yaml
variants: [авба, бавба]
variants: [тӏӕ / тӏӕл- / тӏӕме, тӏӕһ / тӏӕһу / тӏӕһри]
variants: [~ / барара / барив]
```

### `derived_from` & `see_also`

**`derived_from`** — link to source entry filenames for derivations and compounds. List semantic head first. Use even when etymology is present. Reconstructed roots: `["*root"]`.

**`see_also`** — semantically related terms: antonyms, parallel formations, co-hyponyms, culturally related items. Don't overuse.

## Orthography

Spelling follows morpheme structure, not surface phonology. Predictable alternations are stated once in the grammar and not encoded in individual spellings. Four conventions apply:

### Citation and Lexicalized Forms

Write what surfaces in the citation form or in lexicalized derived words. Etymological spelling is not used.

- *дис* (abs), despite geminate resurfacing in *диссу-* (obl)
- *ахле* (pl), despite the geminate in *аххал* (abs) — forms written as they surface
- *шимбе* (pl) — suffix *-бе* assimilated the root sonorant of *шин* (sg)

### Inflectional Morpheme Boundaries

Write each morpheme transparently. Never reflect assimilation — consonantal, vocalic, or nasal — at morpheme boundaries.

- *машинла*, *чӏвел-ра*, *азирна* — case suffixes written transparently
- *а-*/*ма-* negation, *ца-*/*ка-*/*ьа-* prefixes, *-их-* causative — written consistently regardless of context: *барихара*, *барихив*, *мабарихелде*

### Verb Paradigm Roots

Write the underlying root form recoverable from the paradigm. The geminate is real and surfaces before vowels; degemination before consonants is predictable and not reflected.

- *биххӕра*, *биххӕв*, *биххне* (despite pronounced *бихне*) — *хх* written consistently throughout

### Word Division (Interim Convention)

Full standardization — compounds, clitics, hyphenation, apostrophe use — is deferred to v1.2 and requires a corpus. Until then, write all components separately regardless of lexicalization degree.

- Compound verbs: *кумек барара*, *сар виһора*, *ул катара*
- Compound nominals/adjectives: *миг бӕрӏив*, *шӕӏ ҡерҡил*, *давла чев*

## Checklist

- [ ] Headword uses correct citation form?
- [ ] Forms don't repeat the headword?
- [ ] Compound verbs: verbal part only?
- [ ] Neutral *-б-* class marker in headword and forms?
- [ ] Etymology or just derived_from?
- [ ] Aliases: correct POS, not redundant?
- [ ] *Italics* for cited forms, "quotes" for glosses?
- [ ] Components written separately (word division)?
