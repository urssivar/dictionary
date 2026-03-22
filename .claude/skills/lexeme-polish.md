---
name: lexeme-polish
description: Advisory review of Kaitag lexeme files against EDITORIAL_GUIDELINES.md.
---

# Lexeme Polish

Advisory review of Kaitag dictionary YAML entries against `EDITORIAL_GUIDELINES.md`. Read the file(s), identify issues, output a concise list. Do not edit anything unless the user explicitly asks.

## When This Skill Applies

- User says "polish", "review", or "check" a file or letter folder
- User finishes editing a letter and asks for a pass

## How to Review

Read `EDITORIAL_GUIDELINES.md` first. For each entry, check against the checklist at the end of the guidelines. Only flag real issues, not hypothetical ones.

Do NOT flag:

- Semantic shift between a loanword's source and its Kaitag meaning — shift on borrowing is normal
- `derived_from` mismatching etymology — they can legitimately point to different bases

## Output Format

For a single file, output issues grouped by category. Only include categories with actual issues:

```
**абаба**
- Examples: definition 1 has no example — consider adding one for clarity
- Aliases: "grandmother" redundant with main translation
```

For a folder, output a table: headword | issues. Skip clean entries entirely. Keep it terse.

## Tone

Advisory, not prescriptive — flag things worth reconsidering, not every imperfection.
