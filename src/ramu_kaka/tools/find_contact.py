"""find_contact: look up contacts by any part of the name. Returns every match."""

from pydantic import Field

from ramu_kaka.sandbox.state import PhoneState, Strict
from ramu_kaka.tools.text_match import matches

NAME = "find_contact"
DESCRIPTION = ("Find contacts by name or part of a name, e.g. 'Rahul' or 'Sharma'. Returns every match "
               "with phone and email. If more than one matches, ask the user which one.")
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    query: str = Field(min_length=1, description="Name or part of a name.")


def run(state: PhoneState, args: Args) -> dict:
    found = [c.model_dump() for c in state.contacts if matches(args.query, c.name)]
    return {"contacts": found, "count": len(found)}
