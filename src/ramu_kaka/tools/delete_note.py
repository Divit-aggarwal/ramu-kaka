"""delete_note: delete one note by ID. Can't be undone, so the user confirms first."""

from pydantic import Field

from ramu_kaka.sandbox.state import PhoneState, Strict

NAME = "delete_note"
DESCRIPTION = ("Delete one note by its ID (e.g. N3). Find the ID with search_notes first. "
               "The user is asked to confirm before it runs.")
RISK = "Confirm first"
VERSION = "v1"


class Args(Strict):
    note_id: str = Field(pattern=r"^N\d+$", description="Note ID from search_notes, e.g. N3.")


def run(state: PhoneState, args: Args) -> dict:
    remaining = [n for n in state.notes if n.id != args.note_id]
    if len(remaining) == len(state.notes):
        return {"error": f"No note with ID {args.note_id}."}
    state.notes = remaining
    return {"deleted": args.note_id}
