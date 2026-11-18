# tools/ — Phase 2

One file per tool: the 18 v1 tools plus the two Blocked holdback tools
(`send_message_silently`, `delete_file`). Each file has a Pydantic argument schema with exact
formats, a fixed risk level and a function that acts on the sandbox `PhoneState`.
Frozen after Phase 1: no new v1 tools.
