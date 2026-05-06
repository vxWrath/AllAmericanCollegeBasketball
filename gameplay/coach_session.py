from typing import Any

from msgspec import Struct

from .models import Career, PlayerStats, Team

__all__ = ["CoachSession"]


class CoachSession(Struct, kw_only=True, dict=True):
    career: Career
    teams: dict[int, Team]
    conferences: dict[str, Any]
    player_stats: dict[int, PlayerStats]

    def __post_init__(self) -> None:
        self.database: Any = None

    async def save(self) -> None:
        raise NotImplementedError

    async def remove(self) -> None:
        raise NotImplementedError
