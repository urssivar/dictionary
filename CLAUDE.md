# Kaitag Dictionary

A bilingual (English/Russian) dictionary of the Kaitag language, a Northeast Caucasian language.

## Project Structure

```
lexicon/[letter]/   — lexeme YAML files, one per entry
data/tags.yaml      — complete tag taxonomy (grammar, etymology, register, semantic)
data/               — other reference tables
.vscode/lexeme-schema.json  — JSON schema for lexeme files
.claude/EDITORIAL_GUIDELINES.md  — editorial rules and conventions
.claude/skills/lexeme-polish/    — polish/review skill
```

## Workflow

- Lexemes are authored and edited manually by the user
- After finishing a letter, the user requests a polish pass: "check lexicon/[letter]"
- The polish skill reads all entries and outputs an advisory report — no edits unless explicitly asked

## Key Conventions

- All valid tags are defined in `data/tags.yaml` — never invent tags
- Semantic tags go at definition level; grammar/etymology/register tags go at entry level
- Full editorial rules are in `.claude/EDITORIAL_GUIDELINES.md`
