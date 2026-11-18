"""recall_facts: look up stored facts by key words."""

from pydantic import Field

from ramu_kaka.sandbox.state import PhoneState, Strict
from ramu_kaka.tools.text_match import matches

NAME = "recall_facts"
DESCRIPTION = ("Look up stored facts about the user by key words, e.g. 'room' or 'laptop'. "
               "Every word must appear. An empty query returns all facts.")
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    query: str = Field(description="Key words. Empty string = all facts.")


def run(state: PhoneState, args: Args) -> dict:
    facts = [f.model_dump() for f in state.facts if matches(args.query, f.text)]
    return {"facts": facts, "count": len(facts)}
