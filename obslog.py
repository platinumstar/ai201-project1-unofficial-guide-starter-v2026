"""obslog.py — append one JSON line per request to logs/requests.jsonl.

Usage:
    from obslog import log_event
    log_event(status=200, latency_ms=412, question="...", sources=[...])

Logging must never break a request, so every failure here is swallowed.
"""

import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs") / "requests.jsonl"
MAX_LOG_BYTES = 5 * 1024 * 1024  # stop appending past this so a flood cannot fill the disk


def log_event(**fields) -> None:
    record = {"ts": datetime.now().isoformat(timespec="seconds"), **fields}
    try:
        LOG_PATH.parent.mkdir(exist_ok=True)
        if LOG_PATH.exists() and LOG_PATH.stat().st_size > MAX_LOG_BYTES:
            return
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:  # noqa: BLE001 — a logging problem must not fail the request
        pass
