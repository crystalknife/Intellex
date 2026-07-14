"""
Keyword Service

Extracts keywords using spaCy noun chunks + named entities, ranked by
frequency and weighted toward the title. This intentionally favors
multi-word phrases and proper nouns -- the terms that actually
distinguish one story from another -- over keeping every individual
noun/adjective in the document unranked. The previous approach produced
noisy, low-signal keyword sets (e.g. "able", "obvious", "invisible")
that made keyword-overlap event clustering unreliable in practice.
"""

import re
from collections import Counter

import spacy

nlp = spacy.load("en_core_web_sm")

# Generic terms that surface constantly in noun-chunk extraction but
# carry no signal for distinguishing one story from another.
_GENERIC_STOP_TERMS = {
    "today", "yesterday", "tomorrow", "week", "weeks", "month", "months",
    "year", "years", "day", "days", "hour", "hours", "minute", "minutes",
    "time", "way", "thing", "things", "people", "world", "report",
    "story", "news", "article", "post", "part", "lot", "bit",
}

_LEADING_DETERMINER = re.compile(
    r"^(the|a|an|this|that|these|those|its|his|her|their)\s+"
)

_EDGE_PUNCT = re.compile(r"^[\s,.;:!?\-\"']+|[\s,.;:!?\-\"']+$")

_MAX_KEYWORDS = 12

# Entity types that are technically valid NER output but add noise
# rather than signal when treated as keywords (e.g. "years", "today",
# "4").
_LOW_VALUE_ENTITY_LABELS = {"DATE", "TIME", "CARDINAL", "ORDINAL", "PERCENT"}


def _clean_phrase(text: str) -> str:
    text = text.strip().lower()
    text = _LEADING_DETERMINER.sub("", text).strip()
    text = _EDGE_PUNCT.sub("", text).strip()
    return text


class KeywordService:
    """Service responsible for keyword / key-phrase extraction."""

    @staticmethod
    def extract(text: str, title: str = "") -> list[str]:
        if not text.strip():
            return []

        doc = nlp(text)
        counts: Counter[str] = Counter()

        # Multi-word noun phrases are the highest-signal candidates --
        # "smart home" or "AI data center" mean far more than the
        # individual adjectives/nouns that compose them.
        for chunk in doc.noun_chunks:
            phrase = _clean_phrase(chunk.text)

            if len(phrase) < 3 or phrase in _GENERIC_STOP_TERMS:
                continue

            is_single_word = " " not in phrase

            if is_single_word and (
                phrase in nlp.Defaults.stop_words or len(phrase) < 4
            ):
                continue

            counts[phrase] += 2 if not is_single_word else 1

        # Proper nouns carry identifying signal even when they only ever
        # appear as a modifier inside a longer compound phrase ("NVIDIA"
        # in "NVIDIA GPU shortage" is never the chunk's grammatical head,
        # so the noun-chunk pass above never surfaces it alone). Pulling
        # every PROPN token directly is what lets two articles that
        # phrase the same subject differently still share an exact
        # keyword for clustering purposes.
        for token in doc:
            if token.pos_ != "PROPN":
                continue

            word = token.text.strip().lower()

            if (
                len(word) >= 3
                and word not in _GENERIC_STOP_TERMS
                and word not in nlp.Defaults.stop_words
            ):
                counts[word] += 1

        # Named entities are always relevant regardless of how often
        # they repeat -- a single mention of "NVIDIA" still matters.
        for ent in doc.ents:
            if ent.label_ in _LOW_VALUE_ENTITY_LABELS:
                continue

            phrase = ent.text.strip().lower()

            if 3 <= len(phrase) <= 60 and len(phrase.split()) <= 6:
                counts[phrase] += 3

        # Title terms get the strongest boost: whatever the headline
        # names is definitionally what the story is about, even if it
        # only appears once in the body.
        if title:
            for chunk in nlp(title).noun_chunks:
                phrase = _clean_phrase(chunk.text)

                if len(phrase) >= 3:
                    counts[phrase] += 4

        if not counts:
            return []

        ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))

        return [term for term, _ in ranked[:_MAX_KEYWORDS]]
