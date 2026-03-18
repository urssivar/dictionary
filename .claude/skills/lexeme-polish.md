---
name: lexeme-polish
description: This skill should be used when the user asks to "polish", "review", or "check" a lexeme file or an entire letter folder in the Kaitag dictionary. Provides a concise advisory review of a YAML lexeme entry or all entries in a folder against editorial guidelines.
---

# Lexeme Polish

Advisory review of Kaitag dictionary YAML entries against `EDITORIAL_GUIDELINES.md`. Read the file(s), identify issues, output a concise list. Do not edit anything unless the user explicitly asks.

## When This Skill Applies

- User says "polish", "review", or "check" a file or letter folder
- User finishes editing a letter and asks for a pass

## Review Checklist

For each entry, check — only flag real issues, not hypothetical ones. See `EDITORIAL_GUIDELINES.md` for the rules behind each criterion.

1. **Grammar tags** — POS present; verbs have `tr`/`ntr` and `cls` if needed; loanwords have etymology tag
2. **Translations** — verbs use "to + inf"; nouns singular unless plurale tantum; en/ru consistent
3. **Aliases** — correct POS, not redundant with translation, both languages present
4. **Forms** — headword not repeated; compound verbs list verbal part only; syncretic glosses comma-separated
5. **Notes** — only flag if misleading or clearly missing for a culturally opaque term
6. **Etymology** — present for loanwords with correct format; omitted for transparent derivations; do NOT flag on derived forms whose base loanword is already an entry
7. **Examples** — present for common/ambiguous words; each illustrates its own definition; both languages
8. **Cross-references** — `derived_from` for derivations/compounds; `see_also` for related terms; reconstructed roots use `*` prefix
9. **Field order** — Block 1: id, headword, ipa, tags, forms / Block 2: definitions / Block 3: note, etymology, variants, derived_from, see_also; blank lines between blocks

## Output Format

For a single file, output issues grouped by criterion. Only include criteria with actual issues:

```
**абаба**
- Examples: definition 1 has no example — consider adding one for clarity
- Aliases: "grandmother" redundant with main translation
```

For a folder, output a table: headword | issues. Skip clean entries entirely. Keep it terse.

## Tone

- Advisory, not prescriptive — flag things worth reconsidering, not every imperfection
- Do NOT flag semantic shift between a loanword's source and its Kaitag meaning — shift on borrowing is normal
- Do NOT flag `derived_from` mismatching etymology — they can legitimately point to different bases

## Tag Review Notes

Hard-won lessons from the а-letter pass:

- Don't force `culture` on abstract social nouns — only use it for concrete cultural practices/objects
- `disease` is for conditions, not substances or procedures
- `material` is for raw substances, not objects made from them
