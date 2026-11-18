"""get_datetime: today's date, weekday and time, or the date N days from today."""

from datetime import datetime, timedelta

from pydantic import Field

from ramu_kaka.sandbox.state import PhoneState, Strict

NAME = "get_datetime"
DESCRIPTION = ("Get the current date, weekday and time. Use add_days to get another day: 1 = tomorrow, "
               "4 = four days from now. Use this before working out 'tomorrow', 'Friday' or 'in 3 days'.")
RISK = "Safe"
VERSION = "v1"


class Args(Strict):
    add_days: int = Field(default=0, ge=-3660, le=3660, description="Days from today. 0 = today, 1 = tomorrow.")


def run(state: PhoneState, args: Args) -> dict:
    now = datetime.strptime(state.now, "%Y-%m-%dT%H:%M")
    day = now + timedelta(days=args.add_days)
    return {"date": day.strftime("%Y-%m-%d"), "weekday": day.strftime("%A"),
            "time_now": now.strftime("%H:%M"), "timezone": state.timezone}
