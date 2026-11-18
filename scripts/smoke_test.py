"""Phase 0 smoke test: does a local LFM2 model return a tool call?

Usage: start `llama-server -m <model.gguf> --port 8080 --jinja` first, then run
`uv run python scripts/smoke_test.py [model-name]`.
"""

import json
import sys
import time

from openai import APIConnectionError, OpenAI

TOOLS = [
    {
        "name": "create_reminder",
        "description": "Create a reminder that fires at a specific date and time.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "What to remind the user about."},
                "time": {
                    "type": "string",
                    "description": "When to fire, as ISO 8601 local time YYYY-MM-DDTHH:MM, e.g. 2026-11-19T17:00.",
                },
            },
            "required": ["text", "time"],
        },
    }
]

# LFM2's native format: tools go inside the system message, between special markers.
SYSTEM = f"List of tools: <|tool_list_start|>{json.dumps(TOOLS)}<|tool_list_end|>"
USER = "Remind me to call Rahul at 5pm."


def main() -> None:
    model = sys.argv[1] if len(sys.argv) > 1 else "lfm2"
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="none")  # llama-server ignores the key

    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": USER}],
            temperature=0,
            max_tokens=128,
        )
    except APIConnectionError:
        sys.exit("Could not reach http://localhost:8080. Start llama-server first (see docstring).")
    elapsed = time.perf_counter() - start

    message = response.choices[0].message
    usage = response.usage
    print(f"raw reply:         {message.content!r}")
    if message.tool_calls:  # with --jinja the server may move a recognised call here
        print(f"tool_calls field:  {message.tool_calls}")
    print(f"prompt_tokens:     {usage.prompt_tokens if usage else '?'}")
    print(f"completion_tokens: {usage.completion_tokens if usage else '?'}")
    print(f"total time:        {elapsed:.2f}s")
    timings = (response.model_extra or {}).get("timings")  # llama-server extra, not OpenAI standard
    if timings:
        print(f"gen tok/s:         {timings['predicted_per_second']:.1f}  (prompt tok/s: {timings['prompt_per_second']:.1f})")

    if usage and usage.prompt_tokens < 50:
        print("WARNING: prompt_tokens < 50 -- tools probably didn't reach the model.")


if __name__ == "__main__":
    main()
