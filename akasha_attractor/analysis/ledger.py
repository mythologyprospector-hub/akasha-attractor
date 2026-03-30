from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from pathlib import Path


def connect(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def fetch_events(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        "SELECT event_id, timestamp, location, category, source, payload_json, confidence FROM events ORDER BY timestamp ASC"
    ).fetchall()

    out = []
    for row in rows:
        item = dict(row)
        payload_json = item.get("payload_json") or "{}"
        try:
            item["payload"] = json.loads(payload_json)
        except Exception:
            item["payload"] = {}
        out.append(item)
    return out
