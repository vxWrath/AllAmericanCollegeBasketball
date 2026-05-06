from typing import TYPE_CHECKING, Any

from msgspec import Struct

from ..utils import MISSING

if TYPE_CHECKING:
    from ..coach_session import CoachSession
    from .game_log import GameLog
    from .player import Player

__all__ = ["Team", "TeamAccomplishments"]


class TeamAccomplishments(Struct, kw_only=True, dict=True):
    conf_championships: int = 0
    conf_tournament_championships: int = 0
    ncp_appearances: int = 0
    ncp_championships: int = 0
    scp_appearances: int = 0
    scp_championships: int = 0
    best_ncp_finish: int | None = None      # 1 = champion, 2 = runner-up, 4 = Final Four, etc.
    best_regular_season_rank: int | None = None


class Team(Struct, kw_only=True, dict=True):
    id: int
    career_id: int
    conference: str
    name: str
    primary_color: str

    preseason_rating: float = 0.0
    preseason_rank: int | None = None

    current_rating: float = 0.0
    previous_rating: float = 0.0

    current_rank: int | None = None
    previous_rank: int | None = None

    accomplishments: TeamAccomplishments = TeamAccomplishments()

    def __post_init__(self) -> None:
        self.game_log: dict[int, GameLog] = {} # week by week log of games played, indexed by week number
        self.players: list[Player] = []
        self.coach_session: CoachSession = MISSING
        self.meta: dict[str, Any] = {}  # conference prestige, tier, etc. from conferences.json

