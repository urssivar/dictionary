# Kaitag Dictionary Guidelines

## Scope

**Deverbal forms** — Kaitag preterites regularly function as adjectives (_бәрӏив_ "cold" from _бурӏара_ "to cool"); negated/derived stems lexicalize as nouns (_адиккнус_ "inhospitable person"). Add as a separate entry with the `vb` tag and `derived_from` when frequent or lexicalized enough.

**Skip** lexically transparent productive patterns: causatives (_X барара_ "to make X"), inchoatives (_X бирһора_ "to become X"), regular adverbs with _-ле_, etc. These are grammar, not lexicon.

**Fixed multi-word terms are lexemes — give them entries, not just examples.** A multi-word expression that names a specific conventional referent is a lexical unit even when its parts are transparent: _ләӏбар ҡати_ "ushanka" (not "any long-eared hat"), the compound-verb _алав биркара_ "to evade" (not "to occur around"). Link the parts with `derived_from`, semantic head first. The test: a settled, specific referent → entry; a free, ad-hoc, productive description → example.

## Structure

**Homonyms vs. polysemy** — keep related senses in **one** entry with multiple `definitions`; a motivated extension is polysemy, not a collision (`person` → `guest`; `fruit` → `tree`). Use separate homonym files only for unrelated words sharing a form: first entry `word.yaml`, then `word-2.yaml`, `word-3.yaml`. A minimal pair with distinct meanings is two lexemes, not two senses (the hummed _мһ_ "yes" vs. _мӏ_ "no").

Four blocks separated by blank lines. Full schema at `.vscode/entry-schema.json`.

`validate.py` enforces: headword/filename match, correct letter folder, valid tags, resolved cross-references, and the etymology prose conventions (`utils/etymology.py`). The schema enforces field types and required fields. The guidelines below cover judgment calls not caught by tooling.

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

Required when applicable: `tr`/`ntr` for verbs, `cls` for class-agreeing words (any POS), `pl` for pluralia tantum nouns. Class agreement can itself carry number — see [Number patterns](#number-patterns).

Use semantic tags sparingly — concrete content words only. Don't tag particles or abstract grammatical words. In particular:

- `culture` — concrete practices/objects, not abstract social nouns
- `disease` — conditions only, not substances or procedures
- `material` — raw substances, not objects made from them

### `translation` & `aliases`

**Form of the translation:**

- Verbs: English infinitive with "to" (`to walk`); Russian imperfective infinitive (`ходить`)
- Nouns: singular unless plurale tantum
- Adjectives: English base form (`cold`); Russian masculine singular (`холодный`)

**The head carries the meaning; parentheses carry supplementary help.** The deciding question is never "precise vs. plain" or "literal vs. figurative" — it is _is this what the word means_ (head) _or extra help_ (parens). The most accurate rendering of the sense heads the gloss.

Parentheticals carry only these functions (closed set):

- **sense restriction** — `howl (of a wolf)` / `вой (волчий)`
- **clarification** of an unfamiliar or technical term — `heifer (young female cow)`, `kunak (sworn guest-friend)`, `ushanka (fur cap with ear flaps)`. Calibrate per language: gloss `kunak` for the English reader, but Russian `кунак` is established and needs none. Match the term's precision to the source — if the source is vaguer than the precise English term, use a vaguer head or push the fine detail to `note`.
- **literal idiom gloss** — figurative meaning fronted, literal in parens: `very far (lit. "at dragon's hut")` / `очень далеко (букв. "в шалаше у дракона")`
- **proper-noun / place type** — name first, type lowercase: `Adaga (village)` / `Адага (село)`. Spell the type out, both languages; no abbreviations (`v.`, `с.`). Type words are a closed paired set in `meta/` — and the mapping is not 1:1 (село/деревня → village; район/область/край/республика must be mapped explicitly). Which district a place sits in → `note`.
- **functional descriptor + equivalents** for particles and other function words (below)

Not allowed: referent or situational commentary — e.g. appending `(inflation)` to a sentence that merely describes an inflationary scene. That belongs in `note`, or is dropped.

**Particles, interjections, function words** — give a functional descriptor with equivalents. Two shapes, by whether a usable target equivalent exists:

- equivalent exists → **equivalent heads, descriptor restricts**: `ugh, oof (of difficulty)` / `ох (от трудности)`
- no single equivalent fits → **descriptor heads, equivalents illustrate**: `dismay or astonishment (oh my, good grief)` / `досада или удивление (ну надо же, ничего себе)`

Drop the POS term only when a natural non-POS noun head replaces it — interjections get one (`expression of …`, `dismay or astonishment`), and the tag already carries "interjection". **Keep** the POS for particles: dropping it strands a bare adjective (`вопросительная` _what?_), so `interrogative particle (really?, is it true?)` / `вопросительная частица (разве?, правда ли?)`. `en` and `ru` must name the **same** function (interjection = междометие, not "восклицание"; emphatic = усилительная, not "просительная"). For an interjection spanning a range, lead with `[emotion-A] or [emotion-B]` and choose straddling equivalents.

**Differentia goes in the translation, not `note`.** Sense-distinguishing content is part of the gloss: `reproach (over past failures)`, not a separate note describing it. `note` is for context _beyond_ the definition.

**Gloss punctuation:** comma separates co-glosses of a single sense (`manners, etiquette`; Russian `а` = `but, and`); semicolon separates distinct senses (`to be; to be able`).

**Aliases** — a search index for discoverability, optimized for recall. **May cross part of speech**; `en` and `ru` need not be parallel. Don't repeat the main translation, don't list another sense's headword, and avoid terms so generic they would surface the entry for unrelated queries.

```yaml
definitions:
  - translation:
      en: inhospitable person
      ru: негостеприимный человек
    aliases:
      en: [unwelcoming, unfriendly]
      ru: [недоброжелательный, неприятный]
```

### `note` & `examples`

**Note** — context the definition itself doesn't carry: cultural/technical clarification, usage, kinship specifics. Not the meaning (translation) and not the differentia (also translation). One or two sentences; full sentences take a period, nominal labels don't.

Level follows the rule that grammar is entry-level: a lexeme-wide property (number behaviour, a default referent shared across senses) sits in the word-level `note`; a property of one sense sits on that definition.

Usage tendencies are `note` material, not tags — "usually plural" / "обычно мн. ч." is a tendency, whereas the `pl` tag is strict pluralia tantum (no singular at all). (A controlled tag for recurring tendencies — `usu-pl`, `coll-sg` — is a v1.2 option; prose for now.)

**Examples** — natural, idiomatic usage illustrating the specific definition. Include at least one for common or ambiguous words.

- Render **naturally in the target language** — examples are translations, not interlinear glosses. Supply the articles English needs (`the story's end`, not `story's end`; default to definite `the` when the source is unmarked) and the objects it needs (`That man gave it.`). Telegraphic, article-dropping register belongs only to `(lit. "…")` glosses.
- Strip framing that doesn't bear on the headword, but keep characteristic frames — especially case government (`на виноградник`, motion-to). Don't compact toward a template; each example stays a plausible utterance.

### `etymology`

Include for loanwords and non-obvious internal formations. Omit for transparent derivations (use `derived_from`) and for derived forms whose base loanword already has its own entry.

One sentence per language: capitalized, terminal period. A sentence opening with a cited form keeps it lowercase (_*ахрей* does not occur independently._).

**Markup** — _italics_ for cited forms (reconstructions take a leading `*`, escaped `\*` in Markdown); "double quotes" for glosses; (parentheses) for supplementary notes; `cf.` / `ср.` for comparanda (see [`cf.` vs. `see_also`](#derived_from--see_also)); `→` for sound change. Gloss punctuation as above: comma = co-glosses of one sense, semicolon = distinct senses.

#### Loanwords

Cite the source form and gloss it. Two principles fix the rest: **transliterate only Perso-Arabic-script sources** (Arabic, Persian); **gloss the source unless the reader is presumed to know it** — a Russian reader needs no gloss for a Russian word, so `ru` omits it. Cite each source in its native orthography; Azerbaijani in **Latin**, not Cyrillic.

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

**Chains** — immediate donor with "from", ultimate origin with "ultimately from" / "восходит к". Don't let a bare ", from" stand in the ultimate slot.

```yaml
etymology:
  en: From Kumyk *авара* "worry", ultimately from Persian آواره (*âvâre*) "vagabond".
  ru: От кумыкского *авара* "беспокойство", восходит к персидскому آواره (*âvâre*) "бродяга".
```

#### Internal derivations

Name the morphological relationship with a grammatical term (closed set below); gloss only the **base lexeme**, and only the sense relevant to this derivation. Intermediate forms are named by category, not glossed.

Two label shapes, by whether the headword **is** the form or is **derived from** it:

- **Identity** (headword = the form): bare noun phrase — no article, no "From".

```yaml
etymology:
  en: Negative stem of *биккара* "to want".
  ru: Отрицательная основа от *биккара* "хотеть".
```

```yaml
etymology:
  en: Contraction of *абиһолли*, negative conditional of *бирьора* "to be".
  ru: Сокращение от *абиһолли*, отрицательной условной формы *бирьора* "быть".
```

- **Derivation** (headword built _from_ the form): `From the …` — the article is natural inside the prepositional phrase.

```yaml
etymology:
  en: From the negative stem of *биккара* "to want" (cf. *буснус* "sleepy person").
  ru: От отрицательной основы глагола *биккара* "хотеть" (ср. *буснус* "соня").
```

`en` and `ru` must name the **same category**; surface phrasing follows each language's idiom (en `Negative of`, ru `Отрицательная форма от` — both name "negative", ru adds форма). Use `от` before the base even where it seems droppable — Kaitag forms don't decline in Russian, so `от` carries the relation. Where two `от` would collide, insert `глагола`: `От отрицательной основы глагола *биккара*` (not `…основы от *биккара*`).

Closed grammatical-term set, `en` ↔ `ru`:

| en                   | ru                           |
| -------------------- | ---------------------------- |
| root                 | корень                       |
| stem                 | основа                       |
| participle           | причастие                    |
| converb              | деепричастие                 |
| masdar (verbal noun) | масдар                       |
| preterite            | претерит                     |
| conditional          | условная форма               |
| negative conditional | отрицательная условная форма |
| habitual present     | настоящее общее              |

Modifiers combine compositionally with these (not frozen strings): `negative` / отрицательн-, `present` / настоящ-, `past` / прошедш-, `hypothetical` / гипотетическ-. The Russian modifier agrees in gender with its head (причастие n. → -ое, форма f. → -ая, основа f. → -ая). The grammatical "negative" is **отрицательн-**, never негативн-.

Negation builds a **stem**, not a root (root = irreducible core: `бикк` is the root, `абикк` = `а-` + root = a stem). Use stem / основа for negated forms unless the analysis genuinely fuses the prefix into the root.

#### Uncertainty

Hedge with a fixed paired ladder: "Probably" / "Вероятно", "Possibly" / "Возможно", "Perhaps related to" / "Может быть связано с".

### `variants`

Plain string array of dialectal/alternative forms. For variants with their own paradigm, slash-separate forms **with no spaces**; use `~` for forms matching the headword. Include an oblique dash `-` directly in the string:

```yaml
variants: [авба, бавба]
variants: [тӏә/тӏәл-/тӏәме, тӏәһ/тӏәһу/тӏәһри]
variants: [~/барара/барив]
```

**Spacing is structural: a space separates compound parts; an unspaced slash separates paradigm forms.** For partial variants of compound words, position mirrors the headword's order, and `~` stands for the part (or paradigm slot) matching the headword:

```yaml
variants: [~ аргара/агара/агур]   # same nominal, variant verbal paradigm
variants: [аххал ~]             # variant nominal, same verbal
```

(Rendering note: expansion of `~` against the headword for display belongs to the export tooling — deferred to v1.1.1.)

### `derived_from` & `see_also`

**`derived_from`** — link to source entry filenames for derivations and compounds. List semantic head first. Use even when etymology is present. Reconstructed roots: `["*root"]`.

**`see_also`** — semantically related terms: antonyms, parallel formations, co-hyponyms, culturally related items. The default home for "related entry" pointers. Don't overuse.

**`cf.` vs. `see_also`** — `cf.` in etymology is reserved for comparanda doing **etymological** work: a parallel formation, a polarity counterpart, the actual base. If a word is named only because it is related, it goes in `see_also` alone and the `cf.` is redundant. When a comparand both explains the formation and is worth navigating to, it may sit in both (e.g. `абиккан` cites `cf. *биккан*` — the positive base it negates — and lists `биккан` in `see_also`).

## Number patterns

**Collective botanical number** (fruits, nuts, grains, and similar). The **singular form** covers one fruit/grain, _many_ fruits/grains (count plurality shown by plural class agreement on verbs/copulas/adjectives), and a single tree/field. The **morphological plural** is reserved for **multiple trees/fields** only.

Record as **one lexeme with two senses** — (1) the fruit/grain and its substance, (2) the plant-locus (tree/field) — with the morphological plural belonging to sense 2. Order senses by the word's prototype (apple → fruit first; wheat → grain first). Put a short, sense-scoped note on the fruit/grain sense:

```yaml
note:
  en: no plural form
  ru: без формы мн. ч.
```

This is accurate _because_ it is scoped to that sense (the locus sense does pluralize). The full pattern lives here, once; entries only point to it. Two underlying rules:

1. count plurality of the fruit/grain is singular-form + plural class agreement (no morphological plural);
2. the morphological plural exists only for the locus (tree/field) sense.

Sense-scoped `forms` (so the plural can attach to one sense) is a v1.2 schema item; until then the note carries it.

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

## Deferred to v1.2

Structural questions logged as known gaps, not half-resolved (require the Oxford Guide review and/or a corpus):

- **Sense-scoped `forms` / number** — so the morphological plural can attach to one sense (collective botanical number; nouns whose number behaviour differs by sense).
- **Example-level `note`** — to gloss an example's idiomaticity or import without polluting its translation.
- **Form-level `note`** — so number-restricted forms self-document in `forms`.
- **Controlled tendency tags** — `usu-pl`, `coll-sg`, etc., replacing recurring prose notes.
- **Noun-class annotation** — class agreement is doing semantic work (number, reference); may warrant richer annotation than the `cls` flag.
- **Word division** — see Orthography above.

`meta/` reference sets to formalize: etymology vocabularies (term pairs, modifiers, hedges, source list); the place-type paired vocabulary.

## Checklist

- [ ] Headword uses correct citation form?
- [ ] Forms don't repeat the headword?
- [ ] Compound verbs: verbal part only?
- [ ] Neutral _-б-_ class marker in headword and forms?
- [ ] Fixed multi-word term → its own entry (not buried as an example)?
- [ ] Related senses in one entry; unrelated collisions as homonym files?
- [ ] Translation: meaning in the head; only an allowed function in parens?
- [ ] Differentia in the translation, not `note`?
- [ ] Particles keep the POS label; interjections drop it for a noun head?
- [ ] Function-word descriptor: `en`/`ru` name the same function?
- [ ] Aliases: not redundant, not generic, not another sense's headword (cross-POS is fine)?
- [ ] Examples render naturally (articles, objects); characteristic frame kept?
- [ ] Collective botanical: one lexeme, two senses, "no plural form" on the fruit/grain sense?
- [ ] Etymology or just `derived_from`?
- [ ] Etymology: identity label (bare) vs. derivation (`From the …`); term from the closed set; same category `en`/`ru`?
- [ ] _Italics_ for cited forms, "quotes" for glosses; comma vs. semicolon correct?
- [ ] Components written separately (word division)?
