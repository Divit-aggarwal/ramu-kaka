"""create_event: add an event to the calendar. Writes to the real calendar, so the user confirms first."""

from pydantic import Field, model_validator

from ramu_kaka.sandbox.state import DateTime, Event, PhoneState, Strict

NAME = "create_event"
DESCRIPTION = ("Add an event to the calendar with exact start and end times. "
               "The user is asked to confirm before it runs.")
RISK = "Confirm first"
VERSION = "v1"


class Args(Strict):
    title: str = Field(min_length=1, description="Event title.")
    start: DateTime = Field(description="Local date-time YYYY-MM-DDTHH:MM, e.g. 2026-11-21T15:00.")
    end: DateTime = Field(description="Local date-time YYYY-MM-DDTHH:MM, after start.")

    @model_validator(mode="after")
    def _end_after_start(self) -> "Args":
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self


def run(state: PhoneState, args: Args) -> dict:
    event = Event(id=state.new_id("events"), title=args.title, start=args.start, end=args.end)
    state.events.append(event)
    return {"created": event.model_dump()}
