"""set_alarm: an alarm that rings at an exact local date-time."""

from pydantic import Field

from ramu_kaka.sandbox.state import Alarm, DateTime, PhoneState, Strict

NAME = "set_alarm"
DESCRIPTION = "Set an alarm that rings at an exact date and time. Use for waking up; use create_reminder for to-dos."
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    time: DateTime = Field(description="Local date-time YYYY-MM-DDTHH:MM, e.g. 2026-11-20T06:30.")
    label: str | None = Field(default=None, description="Optional short label.")


def run(state: PhoneState, args: Args) -> dict:
    alarm = Alarm(id=state.new_id("alarms"), time=args.time, label=args.label)
    state.alarms.append(alarm)
    return {"created": alarm.model_dump()}
