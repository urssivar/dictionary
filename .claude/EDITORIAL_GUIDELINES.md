# Kaitag Dictionary Editorial Guidelines

## General Principles

### Field Order (with blank line separators)

The full scheme is at `.vscode\lexeme-schema.json`.

```yaml
# Block 1: Metadata
id: [unique identifier]
headword: [main form]
ipa: [pronunciation]
tags: [grammar, etymology, register tags]
forms: [inflected forms]
variants: [dialectal variants]

# Block 2: Content
definitions:
  - translation: [main translation]
    tags: [semantic domain tags]
    aliases: [synonyms and hypernyms]
    note: [clarifications]
    examples: [usage examples]

# Block 3: References
etymology: [origin information]
derived_from: [source headwords]
see_also: [related headwords]
source: [provenance code]
```

## Tags

### Tag Categories

All valid tags are defined in `tags.yaml`:

- **Grammar tags** (top-level): Part of speech, verb features, nominal features
- **Etymology tags** (top-level): Loan sources (arabic, russian, turkic, iranian, neologism)
- **Register tags** (definition-level): pejorative, child
- **Semantic tags** (definition-level): Concrete domains (kinship, animal, food, etc.)

### Tag Usage

- Use sparingly for semantic tags - only for concrete content words
- Don't tag abstract grammatical words (adverbs of manner, particles)
- Verify all tags exist in `lexicon/tags.yaml` taxonomy

## Translations

### Main Translations

- **Verbs**: Always use infinitive with "to" in English: `to walk`, `to eat`
- **Nouns**: Use singular form unless plurale tantum
- **Adjectives**: Use base form
- Translations should be self-sufficient; use commas for clarification if needed

### Aliases

**Purpose**: Search discoverability (not displayed in UI)

**Include**:

- Strict synonyms: `to walk` → `[to stroll, to pace]`
- Hypernyms/categories: `puppy` → `[dog]`, `August` → `[month]`
- Related terms that aid discovery: `bread` → add to specific bread types

**Don't include**:

- Words from different parts of speech (e.g., adjectives for nouns)
- Completely unrelated terms
- The main translation repeated

**Format**:

- Match grammatical form: if translation is `to eat`, aliases are `[to consume, to dine]` not `[consume, dine]`
- English and Russian aliases need not be parallel

## Forms

Use standard Leipzig abbreviations (see <https://en.wikipedia.org/wiki/List_of_glossing_abbreviations>)

### Standard Verb Forms (in order)

```yaml
forms:
  - text: [verb]
    gloss: ipfv
  - text: [verb]
    gloss: pret
  - text: [verb]
    gloss: pfv
```

- Headword is ipfv (except rare cases with only pfv)
- Not all verbs have all three forms — some legitimately have only `ipfv` + `pret`; this is normal and does not require a note

### Noun Forms

```yaml
forms:
  - text: [noun]
    gloss: abs
  - text: [noun]
    gloss: obl
  - text: [noun]
    gloss: pl
```

**Omit forms for transparent compounds**: When a compound's inflection is predictable from its head (final element), don't list forms. Example: *ағула иццала* "cancer" (lit. "poison disease") inflects through *иццала*, so forms are unnecessary.

### Class Agreement

- Use neutral -б- class marker in headwords, forms, and references
- Tag with `cls` when verb has class agreement slots
- Don't list all class variants (б/в/р/д) in forms - class variation is implicit

### Multiple Glosses

**Use periods for portmanteau/fused categories:**

```yaml
gloss: 1.sg.pst # Single form expressing person, number, and tense
```

**Use commas for alternatives/syncretism:**

```yaml
gloss: 1.pl, 2.pl  # Same form serves different functions
gloss: 2.sg, pst   # Polyfunctional form
```

## Etymology

### When to Include

**Always include** for:

- Loanwords (with source language and original form)
- Non-obvious semantic shifts
- Irregular formations

**Omit** for:

- Transparent, productive derivations (use `derived_from` only)
- Regular morphological patterns (negative prefix, -деҳ abstract suffix, etc.)
- Derivations of loanwords via native morphology — if the base loanword is already a separate entry (e.g. *авдалдеҳ* from *авдал*), no `loan` tag or etymology needed on the derived form

### Format for Loanwords

**Arabic/Persian** (non-Latin scripts):

```yaml
etymology:
  en: From Arabic أَبَد (*ʔabad*) "eternity".
  ru: От арабского أَبَد (*ʔabad*) "вечность".
```

**Russian** (Cyrillic):

```yaml
etymology:
  en: From Russian *обои* "wallpaper" (pl.), reanalyzed as singular.
  ru: От русского *обои* (мн. ч.), переосмыслено как ед. ч.
```

- No transcription for Russian in English etymology
- No translation in Russian etymology (word is already in Russian)

**Turkic in Cyrillic** (Kumyk, etc.):

```yaml
etymology:
  en: From Kumyk *гьав* or Azerbaijani *ov* "hunt".
  ru: От кумыкского *гьав* или азербайджанского *ov* "охота".
```

- No transcription for Cyrillic in English
- Use modern orthography (Cyrillic for Kumyk, Latin for Azerbaijani)

**Chains** (borrowed through intermediate language):

```yaml
etymology:
  en: From Kumyk *авара* "worry", ultimately from Persian آواره (*âvâre*) "vagabond".
  ru: От кумыкского *авара* "беспокойство", восходит к персидскому آواره (*âvâre*) "бродяга".
```

### Concise Formulae

- Negatives: `The negative of *verb* "gloss".`
- Participles: `Negative present participle of *verb* "gloss".`
- Don't over-explain productive patterns

### Formatting Conventions

- Use *italics* for cited linguistic forms: *word*
- Use "double quotes" for glosses/meanings in both English and Russian
- Use (parentheses) for supplementary notes: (cf. *word*), (pl.), (мн. ч.)

## Cross-References

### derived_from

- Link to source headwords for derivation/compounding
- For compounds: include both elements `[noun, verb]`
- Use even when etymology is present (for navigation)
- **Reconstructed roots**: Use asterisk prefix `["*root"]` when the base form doesn't exist as a dictionary entry - these are hidden from UI but maintain structured relationships
- **Semantic head first**: The element that determines the core meaning/category, modifiers/specifiers follow

### see_also

- Semantically related terms (antonyms, parallel formations, co-hyponyms)
- Culturally related terms (ingredients, related dishes, etc.)
- Don't overuse - only genuinely useful connections

## Notes

### When to Use

- Cultural/technical clarifications that don't fit in translation
- Specific kinship relationships lacking English/Russian precision
- Regional dish descriptions, specialized terminology

### Keep Brief

- One or two sentences maximum
- Bilingual when needed for clarity

### Formatting

- Full sentences: capitalize and end with a period
- Nominal descriptions (labels, classifications): lowercase, no period

## Examples

### Quality

- Natural, idiomatic usage
- Illustrate the definition, not other definitions
- Include translation in both languages

### When to Include

- At least one for common/ambiguous words
- Optional for very clear, concrete terms
- Multiple examples when word has distinct uses

## Common Mistakes to Avoid

1. **Don't** add aliases from wrong part of speech
2. **Don't** use invalid semantic tags (check tags.yaml)
3. **Don't** forget "to" in English verb infinitives and aliases
4. **Don't** include etymology for transparent derivations
5. **Don't** mix up `pret` and `aor` (use `pret`)
6. **Don't** forget to update field order with blank line separators
7. **Don't** add transcription for Russian/Cyrillic Turkic
8. **Don't** translate Russian words in Russian etymology
9. **Don't** use quotation marks for linguistic forms (use *italics*)
10. **Don't** forget periods at end of schema descriptions

## Consistency Checklist

Before finalizing an entry:

- [ ] Field order correct with blank lines?
- [ ] Verb forms in ipfv, pret, pfv order?
- [ ] All tags valid per tags.yaml?
- [ ] Etymology needed or just derived_from?
- [ ] Aliases appropriate (synonyms/hypernyms, correct POS)?
- [ ] Cross-references added where helpful?
- [ ] Class-agreeing verbs use neutral -б-?
- [ ] Italics for cited forms, quotes for glosses?
- [ ] Bilingual completeness (both en and ru)?
