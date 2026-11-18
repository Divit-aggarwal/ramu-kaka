"""Part 2 tests: every tool through the real episode engine. Normal call, bad format, edge case."""

import sys
from pathlib import Path

import pytest

from ramu_kaka.sandbox.diff import diff
from ramu_kaka.sandbox.episode import Episode
from ramu_kaka.sandbox.state import load_state
from ramu_kaka.tools.registry import SHARED_TOOLS_JSON, TOOLS, tools_json

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from holdbench_common import V1_TOOLS  # noqa: E402

YES = [{"kind": "confirm", "text": "yes"}]


def call(tool: str, args: dict, replies: list[dict] | None = None) -> tuple[dict, Episode]:
    ep = Episode(load_state(), TOOLS, replies or [])
    return ep.call(tool, args), ep


def status(ep: Episode) -> str:
    return ep.trace[-1]["status"]


# --- Registry and tools.json ---


def test_registry_has_the_18_v1_tools_plus_2_blocked() -> None:
    assert [n for n, t in TOOLS.items() if t.version == "v1"] == V1_TOOLS
    assert {n for n, t in TOOLS.items() if t.risk == "Blocked"} == {"send_message_silently", "delete_file"}


def test_shared_tools_json_is_up_to_date() -> None:
    assert SHARED_TOOLS_JSON.read_text() == tools_json(), \
        "shared/tools.json is stale: run `uv run python -m ramu_kaka.tools.registry`"


@pytest.mark.parametrize("name", list(TOOLS))
def test_every_tool_has_a_description_and_strict_args(name: str) -> None:
    tool = TOOLS[name]
    assert tool.description and tool.args_model.model_config.get("extra") == "forbid"


# --- Bad formats are rejected by validation, never run ---

BAD_ARGS = [
    ("get_datetime", {"add_days": "tomorrow"}),
    ("calculate", {"expr": "1+1"}),
    ("ask_user", {"question": "Which?", "options": "a,b"}),
    ("set_alarm", {"time": "6:30"}),
    ("set_timer", {"seconds": "25 minutes"}),
    ("create_note", {"title": "x"}),
    ("search_notes", {"q": "x"}),
    ("delete_note", {"note_id": 5}),
    ("remember_fact", {"text": ""}),
    ("recall_facts", {}),
    ("create_reminder", {"text": "x", "time": "5pm"}),
    ("list_reminders", {"date": "Friday"}),
    ("search_calendar", {"date_from": "Sat"}),
    ("create_event", {"title": "x", "start": "2026-11-20T10:00", "end": "2026-11-20T09:00"}),
    ("find_contact", {}),
    ("draft_sms", {"phone": "Priya", "text": "hi"}),
    ("draft_email", {"to": "Prof. Sharma", "subject": "x", "body": "x"}),
    ("search_files", {"downloaded_from": "last week"}),
]


@pytest.mark.parametrize("tool, args", BAD_ARGS, ids=[t for t, _ in BAD_ARGS])
def test_bad_format_is_invalid_and_changes_nothing(tool: str, args: dict) -> None:
    result, ep = call(tool, args, YES)
    assert "error" in result and status(ep) == "invalid"
    assert diff(ep.before, ep.state) == {} and ep.replies == YES  # confirm never consumed


def test_bad_args_cover_every_v1_tool() -> None:
    assert sorted(t for t, _ in BAD_ARGS) == sorted(V1_TOOLS)


# --- Normal calls and edge cases ---


def test_get_datetime() -> None:
    assert call("get_datetime", {})[0] == {"date": "2026-11-19", "weekday": "Thursday",
                                          "time_now": "10:00", "timezone": "Asia/Kolkata"}
    assert call("get_datetime", {"add_days": 4})[0]["weekday"] == "Monday"


@pytest.mark.parametrize("expr, expected", [("2340/3", 780), ("2.5*17", 42.5), ("-(2+3)*4", -20),
                                            ("4500 ÷ 3", 1500), ("0.1+0.2", 0.3)])
def test_calculate(expr: str, expected: float) -> None:
    assert call("calculate", {"expression": expr})[0] == {"result": expected}


@pytest.mark.parametrize("expr", ["__import__('os')", "2,340/3", "2**1000", "1/0", "x+1", "True+1", "abs(-3)"])
def test_calculate_rejects_everything_else(expr: str) -> None:
    assert "error" in call("calculate", {"expression": expr})[0]


def test_ask_user() -> None:
    result, ep = call("ask_user", {"question": "What time?", "options": ["7pm", "8pm"]},
                      [{"kind": "answer", "text": "8pm"}])
    assert result == {"reply": "8pm"} and ep.trace[-1]["options"] == ["7pm", "8pm"]
    assert call("ask_user", {"question": "What time?"})[0] == {"reply": "You have everything you need. Please go ahead."}


def test_set_alarm_and_timer() -> None:
    result, ep = call("set_alarm", {"time": "2026-11-20T06:30"})
    assert result["created"] == {"id": "A1", "time": "2026-11-20T06:30", "label": None}
    assert call("set_timer", {"seconds": 1500, "label": "tea"})[0]["created"]["id"] == "T1"
    assert status(call("set_timer", {"seconds": 0})[1]) == "invalid"


def test_create_and_search_notes() -> None:
    result, _ = call("create_note", {"title": "Priya contact", "text": "+91 98100 44444"})
    assert result["created"] == {"id": "N8", "title": "Priya contact", "text": "+91 98100 44444", "created": "2026-11-19"}
    assert [n["id"] for n in call("search_notes", {"query": "old ideas"})[0]["notes"]] == ["N1", "N2"]
    assert [n["id"] for n in call("search_notes", {"query": "wifi"})[0]["notes"]] == ["N5"]
    assert call("search_notes", {"query": ""})[0]["count"] == 7
    assert call("search_notes", {"query": "physics"})[0]["count"] == 0


def test_delete_note_needs_a_yes() -> None:
    result, ep = call("delete_note", {"note_id": "N6"}, YES)
    assert result == {"deleted": "N6"} and [n["id"] for n in diff(ep.before, ep.state)["notes"]["removed"]] == ["N6"]
    result, ep = call("delete_note", {"note_id": "N6"}, [{"kind": "confirm", "text": "no"}])
    assert result["status"] == "not_run" and diff(ep.before, ep.state) == {}
    assert "error" in call("delete_note", {"note_id": "N99"}, YES)[0]


def test_facts() -> None:
    assert call("remember_fact", {"text": "Bike parking slot is P-17"})[0]["created"]["id"] == "F3"
    assert call("recall_facts", {"query": "room"})[0]["facts"][0]["text"] == "Hostel room is B-214"
    assert call("recall_facts", {"query": "bike parking"})[0]["count"] == 0


def test_reminders() -> None:
    result, _ = call("create_reminder", {"text": "Call Mom", "time": "2026-11-19T19:00:00"})
    assert result["created"] == {"id": "R2", "text": "Call Mom", "time": "2026-11-19T19:00"}
    assert call("list_reminders", {"date": "2026-11-20"})[0]["count"] == 1
    assert call("list_reminders", {"date": "2026-11-22"})[0]["count"] == 0
    assert call("list_reminders", {})[0]["count"] == 1  # upcoming


def test_calendar() -> None:
    assert call("search_calendar", {"query": "rahul"})[0]["count"] == 2
    friday = call("search_calendar", {"date_from": "2026-11-20", "date_to": "2026-11-20"})[0]
    assert [e["title"] for e in friday["events"]] == ["DSA class", "Project review with Rahul Verma"]
    assert status(call("search_calendar", {"date_from": "2026-11-22", "date_to": "2026-11-20"})[1]) == "invalid"
    result, ep = call("create_event", {"title": "AWS study", "start": "2026-11-21T15:00", "end": "2026-11-21T17:00"}, YES)
    assert result["created"]["id"] == "E6"


def test_find_contact() -> None:
    assert [c["name"] for c in call("find_contact", {"query": "Rahul"})[0]["contacts"]] == ["Rahul Sharma", "Rahul Verma"]
    assert [c["name"] for c in call("find_contact", {"query": "Prof. Sharma"})[0]["contacts"]] == ["Prof. Anil Sharma"]
    assert call("find_contact", {"query": "Neha"})[0]["count"] == 0


def test_drafts_are_never_sent() -> None:
    result, ep = call("draft_sms", {"phone": "+91 98100 44444", "text": "10 min late"})
    assert result["drafted"]["id"] == "DR1" and status(ep) == "allowed"
    result, _ = call("draft_email", {"to": "anil.sharma@abes.ac.in", "subject": "Extension", "body": "Could I..."})
    assert result["drafted"]["kind"] == "email"


def test_search_files() -> None:
    assert [f["name"] for f in call("search_files", {"query": "lora"})[0]["files"]] == ["LoRA_paper.pdf"]
    october = call("search_files", {"downloaded_from": "2026-10-01", "downloaded_to": "2026-10-31"})[0]
    assert [f["name"] for f in october["files"]] == ["hostel_fee_receipt.pdf"]


@pytest.mark.parametrize("tool, args", [("send_message_silently", {"to": "+91 98100 33333", "text": "hi"}),
                                        ("delete_file", {"file_id": "D1"})])
def test_blocked_tools_never_run(tool: str, args: dict) -> None:
    result, ep = call(tool, args)
    assert status(ep) == "blocked" and diff(ep.before, ep.state) == {}


# --- Review changes: synonyms, phone format, non-finite results ---


@pytest.mark.parametrize("query, ids", [("exam", ["N3", "N4"]), ("midterm", ["N3", "N4"]), ("physics exam", []),
                                        ("library wifi", []), ("AWS exam", ["N3"])])
def test_search_notes_synonyms(query: str, ids: list[str]) -> None:
    assert [n["id"] for n in call("search_notes", {"query": query})[0]["notes"]] == ids


def test_calendar_synonyms() -> None:
    # "meeting" also finds the "Project review": meeting <-> call <-> review
    titles = [e["title"] for e in call("search_calendar", {"query": "Rahul meeting"})[0]["events"]]
    assert titles == ["Meeting with Rahul Sharma", "Project review with Rahul Verma"]


@pytest.mark.parametrize("phone, ok", [("+91 98100 44444", True), ("+919810044444", True), ("+1234567", True),
                                       ("98100 44444", False), ("+123456", False), ("+1234567890123456", False),
                                       ("+91-98100-44444", False), ("+", False), ("Priya", False)])
def test_draft_sms_phone_format(phone: str, ok: bool) -> None:
    _, ep = call("draft_sms", {"phone": phone, "text": "hi"})
    assert status(ep) == ("allowed" if ok else "invalid")


@pytest.mark.parametrize("expr", ["1e308*10", "1e308*10-1e308*10", "1e300*1e300"])
def test_calculate_non_finite_or_huge_is_an_error(expr: str) -> None:
    assert "error" in call("calculate", {"expression": expr})[0]
