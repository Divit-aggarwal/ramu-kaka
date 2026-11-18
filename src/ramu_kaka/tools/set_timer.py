"""set_timer: a countdown timer."""

from pydantic import Field

from ramu_kaka.sandbox.state import PhoneState, Strict, Timer

NAME = "set_timer"
DESCRIPTION = "Start a countdown timer. seconds is the total length in seconds: 25 minutes = 1500."
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    seconds: int = Field(ge=1, le=86400, description="Total seconds, e.g. 1500 for 25 minutes.")
    label: str | None = Field(default=None, description="Optional short label.")


def run(state: PhoneState, args: Args) -> dict:
    timer = Timer(id=state.new_id("timers"), seconds=args.seconds, label=args.label)
    state.timers.append(timer)
    return {"created": timer.model_dump()}
