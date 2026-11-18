"""All tools, by name, plus the generator for shared/tools.json.

shared/tools.json is the single source of truth for tool definitions: the Python harness's prompt
and the Kotlin app both read it. Regenerate after changing any tool:
    uv run python -m ramu_kaka.tools.registry
A test fails if the file is out of date.
"""

import json
from pathlib import Path
from types import ModuleType

from pydantic import BaseModel

from ramu_kaka.sandbox.episode import Tool
from ramu_kaka.tools import (
    ask_user, calculate, create_event, create_note, create_reminder, delete_file, delete_note,
    draft_email, draft_sms, find_contact, get_datetime, list_reminders, recall_facts, remember_fact,
    search_calendar, search_files, search_notes, send_message_silently, set_alarm, set_timer,
)

SHARED_TOOLS_JSON = Path(__file__).resolve().parents[3] / "shared" / "tools.json"

# Order = order in tools.json. The 18 v1 tools, then the 2 Blocked holdback tools.
MODULES: list[ModuleType] = [
    get_datetime, calculate, ask_user, set_alarm, set_timer, create_note, search_notes, delete_note,
    remember_fact, recall_facts, create_reminder, list_reminders, search_calendar, create_event,
    find_contact, draft_sms, draft_email, search_files,
    send_message_silently, delete_file,
]

TOOLS: dict[str, Tool] = {
    m.NAME: Tool(name=m.NAME, risk=m.RISK, args_model=m.Args, run=m.run,
                 description=m.DESCRIPTION, version=m.VERSION)
    for m in MODULES
}


def get(name: str) -> Tool | None:
    return TOOLS.get(name)


def plain_schema(model: type[BaseModel]) -> dict:
    """Pydantic's JSON Schema, simplified for small models: no titles or defaults, and
    'string or null' becomes just 'string' (optional = not in 'required')."""
    schema = model.model_json_schema()
    properties = {}
    for name, prop in schema["properties"].items():
        prop = {k: v for k, v in prop.items() if k not in ("title", "default")}
        if "anyOf" in prop:
            not_null = [option for option in prop.pop("anyOf") if option.get("type") != "null"]
            prop = {**not_null[0], **prop}
        properties[name] = prop
    return {"type": "object", "properties": properties, "required": schema.get("required", [])}


def tools_json() -> str:
    tools = [{"name": t.name, "description": t.description, "risk": t.risk, "version": t.version,
              "parameters": plain_schema(t.args_model)} for t in TOOLS.values()]
    return json.dumps(tools, indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    SHARED_TOOLS_JSON.parent.mkdir(exist_ok=True)
    SHARED_TOOLS_JSON.write_text(tools_json())
    print(f"Wrote {SHARED_TOOLS_JSON} ({len(TOOLS)} tools)")
