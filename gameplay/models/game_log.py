from enum import IntEnum

from msgspec import Struct

__all__ = ["GameLocation", "GameType", "GameLog"]


class GameLocation(IntEnum):
    HOME = 0
    AWAY = 1
    NEUTRAL = 2


class GameType(IntEnum):
    NON_CONFERENCE = 0
    CONFERENCE = 1
    CONF_TOURNAMENT = 2
    NCP_TOURNAMENT = 3
    SCP_TOURNAMENT = 4


class GameLog(Struct, kw_only=True, dict=True):
    week: int
    opponent_team_id: int

    location: GameLocation
    type: GameType

    team_overall: float
    opponent_overall: float

    team_score: int = 0
    opponent_score: int = 0
    overtimes: int | None = None

    team_rank_at_time: int | None = None
    opponent_rank_at_time: int | None = None

    team_rating_at_time: float | None = None
    opponent_rating_at_time: float | None = None
