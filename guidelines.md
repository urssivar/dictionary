# Kaitag Dictionary Guidelines

## Scope

**Deverbal adjectives** — Kaitag preterites regularly function as adjectives (_бәрӏив_ "cold" from _бурӏара_ "to cool"). Add as a separate entry with `vb` tag and `derived_from` when frequent or lexicalized enough.

**Skip** lexically transparent productive patterns: causatives (_X барара_ "to make X"), inchoatives (_X бирһора_ "to become X"), regular adverbs with _-ле_, etc. These are grammar, not lexicon. Exception: include compound verbs with non-compositional meaning (e.g. _алав биркара_ "to evade", not literally "to occur around").

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
- Words with class agreement: neutral _-б-_ class marker; tag with `cls`

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

Include for loanwords and non-obvious internal formations. Omit for transparent derivations (use `derived_from`) and for derived forms whose base loanword already has its own entry.

One sentence per language: capitalized, ending in a period. If a sentence must open with a cited form, that form stays lowercase (_*ахрей* does not occur independently._).

**Formatting** — _italics_ for cited forms (reconstructions take a leading `*`, escaped `\*` in Markdown); "double quotes" for glosses; (parentheses) for supplementary notes; `cf.` / `ср.` for comparanda; `→` for sound change. In glosses, a comma separates synonyms of one sense ("manners, etiquette"); a semicolon separates distinct senses ("to be; to be able").

#### Loanwords

Cite the source form and gloss it. Two principles: transliterate only Perso-Arabic-script sources, and gloss the source unless the reader is presumed to know it — a Russian reader needs no gloss for a Russian word, so `ru` omits it.

```yaml
etymology:
  en: From Arabic أَبَد (*ʔabad*) "eternity".
  ru: От арабского أَبَد (*ʔabad*) "вечность".
```

```yaml
etymology:
  en: From Russian *обои* "wallpaper" (pl.), reanalyzed as singular.
  ru: От русского *обои* (мн. ч.), переосмыслено как ед. ч.
```

```yaml
etymology:
  en: From Kumyk *гьав* or Azerbaijani *ov* "hunt".
  ru: От кумыкского *гьав* или азербайджанского *ov* "охота".
```

**Chains** — name the immediate donor with "from", the ultimate origin with "ultimately from" / "восходит к". Don't let a bare ", from" stand in the ultimate slot.

```yaml
etymology:
  en: From Kumyk *авара* "worry", ultimately from Persian آواره (*âvâre*) "vagabond".
  ru: От кумыкского *авара* "беспокойство", восходит к персидскому آواره (*âvâre*) "бродяга".
```

#### Internal derivations

Name the morphological relationship with a grammatical term and gloss only the **base lexeme**. Intermediate forms are identified by category, not glossed — the category is recoverable and lint-checkable; a free gloss is neither.

```yaml
etymology:
  en: Negative of *бартара* "to let, allow".
  ru: Отрицательная форма от *бартара* "давать, оставлять".
```

```yaml
etymology:
  en: Contraction of *абиьолли*, the negative conditional of *бирьора* "to be; to be able".
  ru: Сокращение от *абиьолли*, отрицательной условной формы *бирьора* "быть; мочь".
```

The leading label is a bare noun phrase — `Negative of`, `Contraction of`, `Negative present participle of` — with no "The" or "From". An embedded appositive keeps its natural article (`the negative conditional of`).

Grammatical terms come from a closed set; `en` and `ru` must name the **same** category (surface phrasing follows each language's idiom):

| en                   | ru                           |
| -------------------- | ---------------------------- |
| participle           | причастие                    |
| converb              | деепричастие                 |
| masdar / verbal noun | масдар                       |
| preterite            | претерит                     |
| habitual present     | настоящее общее              |
| conditional          | условная форма               |
| negative conditional | отрицательная условная форма |

A participle (adjectival) is not a converb (adverbial); never pair _participle_ with _деепричастие_ or _converb_ with _причастие_.

#### Uncertainty

Hedge with a fixed ladder, paired across languages: high "Probably" / "Вероятно", medium "Possibly" / "Возможно", low "Perhaps related to" / "Может быть связано с".

### `variants`

Plain string array of dialectal/alternative forms. For variants with their own paradigm, slash-separate forms; use `~` for forms matching the headword. Include oblique dash `-` directly in string:

```yaml
variants: [авба, бавба]
variants: [тӏә / тӏәл- / тӏәме, тӏәһ / тӏәһу / тӏәһри]
variants: [~ / барара / барив]
```

### `derived_from` & `see_also`

**`derived_from`** — link to source entry filenames for derivations and compounds. List semantic head first. Use even when etymology is present. Reconstructed roots: `["*root"]`.

**`see_also`** — semantically related terms: antonyms, parallel formations, co-hyponyms, culturally related items. Don't overuse.

## Orthography

Spelling follows morpheme structure, not surface phonology. Predictable alternations are stated once in the grammar and not encoded in individual spellings. Four conventions apply:

### Citation and Lexicalized Forms

Write what surfaces in the citation form or in lexicalized derived words. Etymological spelling is not used.

- _дис_ (abs), despite geminate resurfacing in _диссу-_ (obl)
- _ахле_ (pl), despite the geminate in _аххал_ (abs) — forms written as they surface
- _шимбе_ (pl) — suffix _-бе_ assimilated the root sonorant of _шин_ (sg)

### Inflectional Morpheme Boundaries

Write each morpheme transparently. Never reflect assimilation — consonantal, vocalic, or nasal — at morpheme boundaries.

- _машинла_, _чӏвел-ра_, _азирна_ — case suffixes written transparently
- _а-_/_ма-_ negation, _ца-_/_ка-_/_һа-_ prefixes, _-их-_ causative — written consistently regardless of context: _барихара_, _барихив_, _мабарихелде_

### Verb Paradigm Roots

Write the underlying root form recoverable from the paradigm. The geminate is real and surfaces before vowels; degemination before consonants is predictable and not reflected.

- _биххәра_, _биххәв_, _биххне_ (despite pronounced _бихне_) — _хх_ written consistently throughout

### Word Division (Interim Convention)

Full standardization — compounds, clitics, hyphenation, apostrophe use — is deferred to v1.2 and requires a corpus. Until then, write all components separately regardless of lexicalization degree.

- Compound verbs: _кумек барара_, _сар виһора_, _ул катара_
- Compound nominals/adjectives: _миг бәрӏив_, _шәӏ ҡерҡил_, _давла чев_

## Checklist

- [ ] Headword uses correct citation form?
- [ ] Forms don't repeat the headword?
- [ ] Compound verbs: verbal part only?
- [ ] Neutral _-б-_ class marker in headword and forms?
- [ ] Etymology or just derived_from?
- [ ] Etymology: `en`/`ru` name the same grammatical category?
- [ ] Etymology: source glossed per the loanword table; grammatical terms from the closed set?
- [ ] Aliases: correct POS, not redundant?
- [ ] _Italics_ for cited forms, "quotes" for glosses?
- [ ] Components written separately (word division)?
