"""create_note: save a new note."""

from pydantic import Field

from ramu_kaka.sandbox.state import Note, PhoneState, Strict

NAME = "create_note"
DESCRIPTION = "Save a new note with a title and text."
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    title: str = Field(min_length=1, description="Short title, e.g. Grocery list.")
    text: str = Field(min_length=1, description="The note's content.")


def run(state: PhoneState, args: Args) -> dict:
    note = Note(id=state.new_id("notes"), title=args.title, text=args.text, created=state.now[:10])
    state.notes.append(note)
    return {"created": note.model_dump()}
