"""search_calendar: find events by title words and/or a date range."""

from pydantic import Field, model_validator

from ramu_kaka.sandbox.state import Date, PhoneState, Strict
from ramu_kaka.tools.text_match import matches

NAME = "search_calendar"
DESCRIPTION = ("Find calendar events by words in the title and/or a date range (inclusive). "
               "Also use it to check if the user is free. Give at least a date range or a query.")
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    query: str | None = Field(default=None, description="Words in the event title, e.g. Rahul.")
    date_from: Date | None = Field(default=None, description="First day YYYY-MM-DD.")
    date_to: Date | None = Field(default=None, description="Last day YYYY-MM-DD (same as date_from for one day).")

    @model_validator(mode="after")
    def _range_in_order(self) -> "Args":
        if self.date_from and self.date_to and self.date_to < self.date_from:
            raise ValueError("date_to must be on or after date_from")
        return self


def run(state: PhoneState, args: Args) -> dict:
    found = [
        e for e in state.events
        if (args.query is None or matches(args.query, e.title))
        and (args.date_from is None or e.end[:10] >= args.date_from)
        and (args.date_to is None or e.start[:10] <= args.date_to)
    ]
    found.sort(key=lambda e: e.start)
    return {"events": [e.model_dump() for e in found], "count": len(found)}
