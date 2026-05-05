import pathlib
from typing import Any

import orjson

__all__ = ["TOTAL_TEAMS", "CONFERENCES"]

CONFERENCE_PATH = pathlib.Path(__file__).parent / "conferences.json"

with open(CONFERENCE_PATH) as f:
    CONFERENCES: dict[str, Any] = orjson.loads(f.read())

TOTAL_TEAMS = sum(len(conference["teams"]) for conference in CONFERENCES.values())
