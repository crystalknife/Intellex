"""
Entity Service

Extracts named entities using spaCy.
"""

from collections import defaultdict

import spacy

# Load the NLP model once
nlp = spacy.load("en_core_web_sm")

# en_core_web_sm occasionally misclassifies an entire headline/title
# fragment as a single entity (e.g. a product-review title tagged as
# ORG). Real organization/person/place names are essentially never this
# long, so spans past these bounds are dropped rather than surfaced.
_MAX_ENTITY_CHARS = 48
_MAX_ENTITY_WORDS = 5


class EntityService:
    """Service responsible for Named Entity Recognition."""

    @staticmethod
    def extract(text: str) -> dict[str, list[str]]:
        """
        Extract entities from text.

        Returns:
            {
                "ORG": [...],
                "PERSON": [...],
                "GPE": [...],
                ...
            }
        """

        if not text.strip():
            return {}

        doc = nlp(text)

        entities = defaultdict(set)

        for entity in doc.ents:
            span = entity.text.strip()

            if not span or len(span) > _MAX_ENTITY_CHARS:
                continue

            if len(span.split()) > _MAX_ENTITY_WORDS:
                continue

            entities[entity.label_].add(span)

        return {
            label: sorted(values)
            for label, values in entities.items()
        }