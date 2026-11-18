"""search_files: find shared files by name and/or download date."""

from pydantic import Field, model_validator

from ramu_kaka.sandbox.state import Date, PhoneState, Strict
from ramu_kaka.tools.text_match import matches

NAME = "search_files"
DESCRIPTION = ("Find files (Downloads, Documents, photos) by words in the file name and/or the date "
               "they were downloaded (inclusive range). Can't see what is inside photos.")
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    query: str | None = Field(default=None, description="Words in the file name, e.g. lora.")
    downloaded_from: Date | None = Field(default=None, description="First day YYYY-MM-DD.")
    downloaded_to: Date | None = Field(default=None, description="Last day YYYY-MM-DD.")

    @model_validator(mode="after")
    def _range_in_order(self) -> "Args":
        if self.downloaded_from and self.downloaded_to and self.downloaded_to < self.downloaded_from:
            raise ValueError("downloaded_to must be on or after downloaded_from")
        return self


def run(state: PhoneState, args: Args) -> dict:
    found = [
        f.model_dump() for f in state.files
        if (args.query is None or matches(args.query, f.name))
        and (args.downloaded_from is None or f.downloaded >= args.downloaded_from)
        and (args.downloaded_to is None or f.downloaded <= args.downloaded_to)
    ]
    return {"files": found, "count": len(found)}
