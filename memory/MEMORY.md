# Kaitag Dictionary — Session Memory

## Project
Bilingual (EN/RU) dictionary of Kaitag, a Northeast Caucasian language. Lexemes in `lexicon/[letter]/` as YAML files. Tags in `data/tags.yaml`. Schema in `.vscode/lexeme-schema.json`. Editorial guidelines in `.claude/EDITORIAL_GUIDELINES.md`.

## Workflow
- User edits a full letter, then asks for a polish pass: "check lexicon/[letter]"
- Polish skill at `.claude/skills/lexeme-polish/SKILL.md` — advisory only, no edits unless asked
- Use inline Python to extract/summarize data rather than reading 100+ files individually

## Current Status (Feb 2026)
- Letter а: completed and polished
- Docs (CLAUDE.md, guidelines, skill) are intentionally rough/adhoc
- **After current iteration (1-2 mo): rewrite all contributor-facing docs properly**, with real examples from the corpus and stabilized conventions

## Key Conventions
- Semantic tags: conservative, only clear matches, existing tags only
- `loan` tag not needed on native derivations of loanwords when base is a separate entry
- Verb forms: ipfv-only or ipfv+pret is normal, no note required
- Note formatting: full sentences → capitalize + period; nominal labels → lowercase, no period
- Semantic shift on borrowing is normal, not worth flagging

## Tag Review Lessons (letter а)
- Don't force `culture` onto abstract social nouns (buddy, chore)
- Don't use `disease` for substances (venom) or procedures (surgery)
- Don't use `material` for objects made from materials (coin)
- Future tags to add when ready: `health`, `language`, `behavior`
