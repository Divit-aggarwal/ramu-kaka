"""The fake phone: Pydantic models for everything a task can read or change.

Load the starting phone with `load_state()`. Each episode works on its own deep copy.
Formats are exact: date-times are local `YYYY-MM-DDTHH:MM` (seconds allowed only as `:00`),
dates are `YYYY-MM-DD`. Anything else is a validation error, never a guess.
"""

import re
from datetime import date, datetime
from pathlib import Path
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator

PHONE_STATE_JSON = Path(__file__).resolve().parents[3] / "holdbench" / "phone_state.json"


def _check_datetime(value: str) -> str:
    """'2026-11-19T17:00' or '2026-11-19T17:00:00' → '2026-11-19T17:00'. No offsets, no 'Z'."""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:00)?", value):
        try:
            return datetime.strptime(value[:16], "%Y-%m-%dT%H:%M").strftime("%Y-%m-%dT%H:%M")
        except ValueError:
            pass  # e.g. month 13
    raise ValueError(f"must be a local date-time YYYY-MM-DDTHH:MM, e.g. 2026-11-19T17:00 (got {value!r})")


def _check_date(value: str) -> str:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError:
            pass
    raise ValueError(f"must be a date YYYY-MM-DD, e.g. 2026-11-19 (got {value!r})")


DateTime = Annotated[str, AfterValidator(_check_datetime)]
Date = Annotated[str, AfterValidator(_check_date)]


class Strict(BaseModel):
    """Base for every model here: unknown fields are an error."""
    model_config = ConfigDict(extra="forbid")


class Contact(Strict):
    id: str
    name: str
    phone: str | None
    email: str | None


class Note(Strict):
    id: str
    title: str
    text: str
    created: Date


class Event(Strict):
    id: str
    title: str
    start: DateTime
    end: DateTime


class Reminder(Strict):
    id: str
    text: str
    time: DateTime


class Fact(Strict):
    id: str
    text: str


class File(Strict):
    id: str
    name: str
    folder: str
    downloaded: Date


class Alarm(Strict):
    id: str
    time: DateTime
    label: str | None = None


class Timer(Strict):
    id: str
    seconds: int
    label: str | None = None


class Draft(Strict):
    id: str
    kind: Literal["sms", "email"]
    to: str  # phone number for sms, email address for email
    subject: str | None = None  # email only
    body: str


# Collection name → ID prefix for new items (N8, R2, E6...).
ID_PREFIX = {
    "contacts": "C", "notes": "N", "events": "E", "reminders": "R", "facts": "F",
    "files": "D", "alarms": "A", "timers": "T", "drafts": "DR",
}
COLLECTIONS = tuple(ID_PREFIX)


class PhoneState(Strict):
    now: DateTime
    timezone: str
    contacts: list[Contact]
    notes: list[Note]
    events: list[Event]
    reminders: list[Reminder]
    facts: list[Fact]
    files: list[File]
    alarms: list[Alarm]
    timers: list[Timer]
    drafts: list[Draft]
    # Highest ID number ever used per collection, so a deleted ID (e.g. N7) is never handed out
    # again. Seeded from the loaded items. Not part of phone_state.json.
    last_ids: dict[str, int] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _seed_last_ids(self) -> "PhoneState":
        for name, prefix in ID_PREFIX.items():
            numbers = [int(i.id[len(prefix):]) for i in getattr(self, name) if i.id[len(prefix):].isdigit()]
            self.last_ids[name] = max(numbers + [self.last_ids.get(name, 0)])
        return self

    def new_id(self, collection: str) -> str:
        """Next free ID for a collection: N8 after N1–N7. Deterministic."""
        self.last_ids[collection] += 1
        return f"{ID_PREFIX[collection]}{self.last_ids[collection]}"


def load_state(path: Path = PHONE_STATE_JSON) -> PhoneState:
    return PhoneState.model_validate_json(Path(path).read_text())
