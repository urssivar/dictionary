---
name: lexeme-polish
description: This skill should be used when the user asks to "polish", "review", or "check" a lexeme file or an entire letter folder in the Kaitag dictionary. Provides a concise advisory review of a YAML lexeme entry or all entries in a folder against editorial guidelines.
version: 1.0.0
---

# Lexeme Polish

Advisory review of Kaitag dictionary YAML entries. Read the file(s), identify issues, output a concise list. Do not edit anything unless the user explicitly asks.

## When This Skill Applies

- User says "polish", "review", or "check" a file or letter folder
- User finishes editing a letter and asks for a pass
- User asks `/polish` on a specific lexeme

## Review Criteria

For each entry, check the following — only flag real issues, not hypothetical ones:

### 1. Grammar tags (top-level `tags:`)
- POS tag present and correct
- Verbs: `tr`/`ntr` present; `cls` if verb has class agreement
- Loanwords: etymology tag present (`arabic`, `russian`, `turkic`, `iranian`)
- Register tag if applicable (`pejorative`, `child`)

### 2. Translations
- Verbs: English uses "to + infinitive"
- Nouns: singular unless plurale tantum
- En/ru translations consistent in meaning (not just literal)
- Not ambiguous or overly broad

### 3. Aliases
- Useful for search (synonyms, hypernyms)
- Correct POS — no adjectives aliasing a noun, etc.
- Not redundant with main translation
- Both `en` and `ru` present if aliases exist

### 4. Notes (`note:` at entry or definition level)
- Only flag if a note seems misleading or if an important cultural/technical clarification is clearly missing and the translation alone is insufficient

### 5. Etymology
- Present for loanwords (with source language + original form)
- Format correct per guidelines: script + transliteration for Arabic/Persian; Cyrillic only for Russian/Turkic
- Omitted correctly for transparent derivations (use `derived_from` instead)
- No transcription for Russian; no translation in Russian etymology

### 6. Examples
- Present for common or ambiguous words
- Each example illustrates its own definition, not another
- Translation present in both languages
- Flag missing examples only for words where usage is non-obvious

### 7. Cross-references
- `derived_from` links to source headwords for compounds/derivations
- `see_also` used for genuinely related terms, not overused
- Reconstructed roots use asterisk prefix `["*root"]`

### 8. Field order
- Block 1: id, headword, ipa, tags, forms, variants
- Block 2: definitions (translation, tags, aliases, note, examples)
- Block 3: etymology, derived_from, see_also, source
- Blank lines between blocks

## Output Format

For a single file, output issues grouped by category. Only include categories with actual issues:

```
**абаба**
- Examples: definition 1 has no example — consider adding one for clarity
- Aliases: "grandmother" redundant with main translation
```

For a folder, output a table: headword | issues. Skip clean entries entirely. Keep it terse.

## Tone

- Advisory, not prescriptive
- Flag things worth reconsidering, not every imperfection
- If something is clearly fine, say nothing
