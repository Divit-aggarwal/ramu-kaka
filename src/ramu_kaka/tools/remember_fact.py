"""remember_fact: store a short fact about the user."""

from pydantic import Field

from ramu_kaka.sandbox.state import Fact, PhoneState, Strict

NAME = "remember_fact"
DESCRIPTION = "Store a short fact about the user for later, e.g. 'Hostel room is B-214'."
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    text: str = Field(min_length=1, description="One short fact as a full sentence.")


def run(state: PhoneState, args: Args) -> dict:
    fact = Fact(id=state.new_id("facts"), text=args.text)
    state.facts.append(fact)
    return {"created": fact.model_dump()}
