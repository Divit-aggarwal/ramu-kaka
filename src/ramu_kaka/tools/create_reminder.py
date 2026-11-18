"""create_reminder: a reminder that notifies the user at an exact local date-time."""

from pydantic import Field

from ramu_kaka.sandbox.state import DateTime, PhoneState, Reminder, Strict

NAME = "create_reminder"
DESCRIPTION = "Create a reminder that notifies the user at an exact date and time."
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    text: str = Field(min_length=1, description="What to remind the user about.")
    time: DateTime = Field(description="Local date-time YYYY-MM-DDTHH:MM, e.g. 2026-11-19T17:00.")


def run(state: PhoneState, args: Args) -> dict:
    reminder = Reminder(id=state.new_id("reminders"), text=args.text, time=args.time)
    state.reminders.append(reminder)
    return {"created": reminder.model_dump()}
