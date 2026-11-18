"""One search rule for every search tool, so the model only has to learn it once.

A query matches if every word in it appears somewhere in the searched text. Case, spaces and
punctuation are ignored, so "wifi" matches "Wi-Fi" and "prof sharma" matches "Prof. Anil Sharma".
An empty query matches everything.

A query word also matches if one of its synonyms appears (SYNONYMS below). The list is small and
explicit on purpose: "exam" finds the "DSA midterm" note, but there is no fuzzy matching beyond it.
Phase 5 replaces this with embedding-based retrieval (search by meaning).
"""

import re

# Each group: any word in the group matches any other. Keep this list short and documented.
SYNONYM_GROUPS = [
    {"exam", "midterm", "test", "quiz", "final"},
    {"meeting", "call", "review"},
]
SYNONYMS: dict[str, set[str]] = {word: group for group in SYNONYM_GROUPS for word in group}


def _compact(text: str) -> str:
    return re.sub(r"[^a-z0-9@]", "", text.lower())


def matches(query: str, *texts: str) -> bool:
    haystack = _compact(" ".join(texts))
    for word in query.split():
        word = _compact(word)
        if not any(option in haystack for option in SYNONYMS.get(word, {word})):
            return False
    return True
