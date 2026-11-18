"""search_notes: find notes whose title or text contains every query word."""

from pydantic import Field

from ramu_kaka.sandbox.state import PhoneState, Strict
from ramu_kaka.tools.text_match import matches

NAME = "search_notes"
DESCRIPTION = ("Find notes by key words. Every word must appear in the note's title or text; case and "
               "punctuation are ignored. Use 1-3 key words, e.g. 'grocery' or 'AWS exam'. "
               "An empty query returns all notes.")
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    query: str = Field(description="Key words, e.g. old ideas. Empty string = all notes.")


def run(state: PhoneState, args: Args) -> dict:
    notes = [n.model_dump() for n in state.notes if matches(args.query, n.title, n.text)]
    return {"notes": notes, "count": len(notes)}
