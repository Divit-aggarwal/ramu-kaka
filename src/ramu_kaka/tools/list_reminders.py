"""list_reminders: reminders on one date, or all upcoming ones."""

from pydantic import Field

from ramu_kaka.sandbox.state import Date, PhoneState, Strict

NAME = "list_reminders"
DESCRIPTION = "List reminders on one date, or all upcoming reminders if no date is given."
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    date: Date | None = Field(default=None, description="Date YYYY-MM-DD, e.g. 2026-11-20. Omit for all upcoming.")


def run(state: PhoneState, args: Args) -> dict:
    if args.date:
        found = [r for r in state.reminders if r.time[:10] == args.date]
    else:
        found = [r for r in state.reminders if r.time >= state.now]
    found.sort(key=lambda r: r.time)
    return {"reminders": [r.model_dump() for r in found], "count": len(found)}
