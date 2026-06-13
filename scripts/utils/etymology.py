"""Etymology prose-convention checks.

Companion to validate.py's structural checks. Covers only closed-vocabulary,
near-zero-false-positive properties of the `etymology` field. Judgment calls
(gloss accuracy, plausibility, whether an etymology is warranted at all) belong
to the entry-polish skill, not here.

Schema validation already guarantees etymology is {en, ru} strings when present;
this guards defensively anyway and returns [] on anything malformed.
"""

import re

# --- Closed vocabularies -----------------------------------------------------
# Lift these to meta/etymology.yaml + a loader if you'd rather edit conventions
# as data than as code (matches the tags.yaml / alphabet.yaml pattern).

# (en lead-in, ru genitive lead-in, written in Perso-Arabic script)
SOURCES = [
    ("Arabic",      "арабского",        True),
    ("Persian",     "персидского",      True),
    ("Russian",     "русского",         False),
    ("Kumyk",       "кумыкского",       False),
    ("Azerbaijani", "азербайджанского", False),
]

# Markers of a multi-source chain -> skip the strict translit check.
CHAIN_MARKERS = ("ultimately from", "восходит к")

# A compound names a native (Kaitag) constituent; its gloss belongs to that
# element, not the foreign source -> skip the single-source checks.
COMPOUND_MARKERS = ("Kaitag", "кайтагского")

TRANSLIT = re.compile(r"\(\*[^*]+\*\)")   # (*ʔabad*)
GLOSS = re.compile(r'"[^"]+"')            # "eternity"
# *\*аккора*  (italic-open + escaped asterisk)
RECONSTRUCTION = "*\\*"


def _single_language(text, lang):
    """Checks internal to one language string."""
    out = []
    s = text.strip()
    if not s:
        return out
    if not s.endswith("."):
        out.append(f"etymology.{lang}: no terminal period")
    # Exempt sentences that legitimately open with a cited form (*ахрей* ...).
    if not s.startswith("*") and s[:1].isalpha() and not s[:1].isupper():
        out.append(f"etymology.{lang}: should start capitalized")
    return out


def check_etymology(etymology):
    """Prose-convention checks for the `etymology` field. Returns list[str]."""
    if not isinstance(etymology, dict):
        return []
    en, ru = etymology.get("en"), etymology.get("ru")
    if not isinstance(en, str) or not isinstance(ru, str):
        return []

    errors = []
    errors += _single_language(en, "en")
    errors += _single_language(ru, "ru")

    is_chain = any(m in en or m in ru for m in CHAIN_MARKERS)
    is_compound = any(m in en or m in ru for m in COMPOUND_MARKERS)
    sources = [s for s in SOURCES if re.search(rf"\b{s[0]}\b", en)]

    # Transliteration / no-gloss by source — only trustworthy on a single
    # foreign source (not chains, not compounds with a native element).
    if len(sources) == 1 and not is_chain and not is_compound:
        name, _ru_name, perso_arabic = sources[0]
        has_translit = bool(TRANSLIT.search(en))
        if perso_arabic and not has_translit:
            errors.append(
                f"etymology: {name} source missing transliteration (*...*)")
        if not perso_arabic and has_translit:
            errors.append(
                f"etymology: {name} source should not be transliterated")
        # A Russian reader needs no gloss for a Russian word.
        if name == "Russian" and GLOSS.search(ru):
            errors.append("etymology.ru: Russian source should not be glossed")

    # Participle (adjectival) and converb (adverbial) must not cross en/ru.
    # \b stops причастие from matching inside деепричастие.
    if re.search(r"\bparticiple\b", en) and re.search(r"\bдеепричастие\b", ru):
        errors.append(
            "etymology: en 'participle' vs ru 'деепричастие' (converb)")
    if re.search(r"\bconverb\b", en) and re.search(r"\bпричастие\b", ru):
        errors.append("etymology: en 'converb' vs ru 'причастие' (participle)")

    # Reconstruction mark must appear in both languages or neither.
    if (RECONSTRUCTION in en) != (RECONSTRUCTION in ru):
        errors.append(
            "etymology: reconstruction mark (*) in one language only")

    return errors
