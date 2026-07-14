"""
Event Builder

Groups related documents into events.
"""

from backend.app.domain.document import Document
from backend.app.domain.event import Event

# Entity types that reliably identify "this is the same story" when they
# match exactly across two documents (an org/person/product name is a
# strong, low-noise signal). Types like DATE/CARDINAL are deliberately
# excluded -- "2026" or "4" matching between two documents says nothing
# about whether they're related.
_STRONG_ENTITY_LABELS = {"ORG", "PERSON", "PRODUCT", "GPE", "EVENT", "WORK_OF_ART"}

# Multi-word keyword phrases are specific by design (see
# KeywordService), which means two articles covering the same story
# rarely repeat an identical phrase verbatim -- one says "NVIDIA GPU
# shortage", the other says "AI chip supply constraints". A lower
# threshold than the old single-word-bag approach used is intentional:
# a couple of exact phrase matches is a much stronger signal now than it
# used to be.
_KEYWORD_OVERLAP_THRESHOLD = 2


def _entity_signal(entities: dict[str, list[str]]) -> set[str]:
    signal: set[str] = set()

    for label, values in entities.items():
        if label not in _STRONG_ENTITY_LABELS:
            continue

        for value in values:
            normalized = value.strip().lower()
            if len(normalized) >= 3:
                signal.add(normalized)

    return signal


class EventBuilder:
    """
    Builds Event objects by grouping related documents based on shared
    entities (primary signal) and keyword overlap (secondary signal).
    """

    @staticmethod
    def build(
        documents: list[Document],
    ) -> list[Event]:

        events: list[Event] = []

        # Running per-event entity signal, kept alongside Event.entities
        # (which preserves original casing for display) since matching
        # needs a normalized, lowercased form.
        event_entity_signals: list[set[str]] = []

        for document in documents:

            matched: Event | None = None
            matched_index: int | None = None

            document_keywords = set(document.keywords)
            document_entity_signal = _entity_signal(document.entities)

            for index, event in enumerate(events):

                shared_entities = document_entity_signal.intersection(
                    event_entity_signals[index]
                )

                keyword_overlap = len(
                    document_keywords.intersection(set(event.keywords))
                )

                if (
                    len(shared_entities) >= 2
                    or (len(shared_entities) >= 1 and keyword_overlap >= 1)
                    or keyword_overlap >= _KEYWORD_OVERLAP_THRESHOLD
                ):
                    matched = event
                    matched_index = index
                    break

            if matched is not None and matched_index is not None:

                matched.document_ids.append(document.id)

                matched.keywords = sorted(
                    set(matched.keywords).union(document_keywords)
                )

                for label, values in document.entities.items():

                    existing = set(matched.entities.get(label, []))

                    matched.entities[label] = sorted(
                        existing.union(values)
                    )

                event_entity_signals[matched_index] = event_entity_signals[
                    matched_index
                ].union(document_entity_signal)

            else:

                events.append(
                    Event(
                        title=document.title,
                        document_ids=[document.id],
                        keywords=sorted(document_keywords),
                        entities=document.entities.copy(),
                    )
                )
                event_entity_signals.append(document_entity_signal)

        return events