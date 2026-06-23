---
name: entry-polish
description: Advisory review of Kaitag entry files against guidelines.md.
---

# Entry Polish

Advisory review of Kaitag dictionary YAML entries against `guidelines.md`. Read the file(s), identify issues, output a concise list. Do not edit anything unless the user explicitly asks.

Apply this skill when:

- User says "polish", "review", or "check" a file or letter folder
- User finishes editing a letter and asks for a pass

## Performance

- **Always use Haiku** for audit agents — these are pattern-matching tasks, not reasoning-heavy
- **Always delegate to a subagent** (Agent tool) — keeps main context clean
- **Disable thinking** before running — it burns context with no benefit here
- `scripts/validate.py` (+ `utils/etymology.py`) handles mechanical checks (tags, schema, IDs, folder, etymology prose conventions); don't re-check those — focus on the judgment calls below
- **File access: use Glob then Read only — never Bash** — Bash triggers permission prompts for every call; Read does not

## How to Review

Read `guidelines.md` first, then check each entry against its checklist. Only flag real issues, not hypothetical ones. The judgment calls worth your attention (the linter can't make these):

- **Examples** — natural target-language rendering (articles, objects English needs), not templatey, decoration stripped but characteristic frames kept, text and translation agreeing (number, deixis)
- **Translation head/parens** — meaning in the head; parenthetical carrying only an allowed function (restriction, clarification, literal gloss, place/proper-noun type, function-word descriptor) and **not** referent or situational commentary
- **Differentia placement** — sense-distinguishing content belongs in the translation, not `note`
- **Particles vs. interjections** — particles keep the POS label, interjections drop it for a noun head; `en`/`ru` naming the _same_ function
- **Etymology judgment** — the _right_ category named (beyond set-membership, which the linter checks); `cf.` earning its etymological place vs. belonging in `see_also`; whether an etymology is warranted at all
- **Aliases** — redundant with the translation, too generic, or another sense's headword
- **Note clarity / level** — entry-level for lexeme-wide properties, sense-level otherwise
- **Semantic tag fitness** — concrete content words only
- **Collective botanical number** — one lexeme / two senses, with the "no plural form" note on the fruit/grain sense, not the locus sense

Do NOT flag:

- Semantic shift between a loanword's source and its Kaitag meaning — shift on borrowing is normal
- `derived_from` mismatching etymology — they can legitimately point to different bases
- Issues already caught by `validate.py` (tags, schema, IDs, folder)
- Deterministic etymology checks `etymology.py` owns — transliteration by source, glossing rules, term/hedge vocabulary, terminal punctuation, `негативн-` vs. `отрицательн-`
- **Cross-POS aliases** — aliases are a search index; crossing part of speech is allowed, not an error
- Absence of v1.2-deferred structure (sense-scoped forms, example- or form-level notes)

## Output Format

For a single file, output issues grouped by category. Only include categories with actual issues:

```bash
**абаба**
- Examples: definition 1 has no example — consider adding one for clarity
- Aliases: "grandmother" redundant with main translation
```

For a folder, output a table: headword | issues. Skip clean entries entirely. Keep it terse.

## Tone

Advisory, not prescriptive — flag things worth reconsidering, not every imperfection. Conventions that are judgment calls (possible differentia-in-note, a parenthetical that may be carrying commentary) are raised for the author to decide, not asserted as errors.
