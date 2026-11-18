"""What changed between two phone states, per collection, matched by item ID."""

from ramu_kaka.sandbox.state import COLLECTIONS, PhoneState

Diff = dict[str, dict[str, list[dict]]]


def diff(before: PhoneState, after: PhoneState) -> Diff:
    """{collection: {"added": [items], "removed": [items], "changed": [{"id", "fields": {name: [old, new]}}]}}.
    Only collections with a change appear, so an empty dict means "nothing was written"."""
    out: Diff = {}
    for name in COLLECTIONS:
        old = {i.id: i.model_dump() for i in getattr(before, name)}
        new = {i.id: i.model_dump() for i in getattr(after, name)}
        added = [new[i] for i in new if i not in old]
        removed = [old[i] for i in old if i not in new]
        changed = [
            {"id": i, "fields": {k: [old[i][k], new[i][k]] for k in new[i] if old[i][k] != new[i][k]}}
            for i in new if i in old and old[i] != new[i]
        ]
        if added or removed or changed:
            out[name] = {"added": added, "removed": removed, "changed": changed}
    return out
