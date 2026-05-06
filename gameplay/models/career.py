import datetime
from typing import Self

from msgspec import Struct, field

__all__ = ["Career", "CoachingStintStats"]


class CoachingStintStats(Struct, kw_only=True, dict=True):
    start_season: int
    end_season: int | None = None

    wins: int = 0
    losses: int = 0

    ncp_appearances: int = 0
    ncp_championships: int = 0
    scp_appearances: int = 0
    scp_championships: int = 0

    reg_conf_championships: int = 0
    conf_tournament_appearances: int = 0
    conf_tournament_championships: int = 0


class Career(Struct, kw_only=True, dict=True):
    id: int
    user_id: int
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC)
    )
    last_played_at: datetime.datetime | None = None

    coach_name: str
    rng_seed: int
    current_season: int
    current_week: int
    current_team_id: int

    coaching_stints: dict[int, CoachingStintStats] = field(default_factory=dict)

    def update_last_played_at(self) -> Self:
        self.last_played_at = datetime.datetime.now(tz=datetime.UTC)
        return self

    def career_length(self) -> int:
        return (
            self.current_season
            - min(stint.start_season for stint in self.coaching_stints.values())
            + 1
        )

    def career_wins(self) -> int:
        return sum(stint.wins for stint in self.coaching_stints.values())

    def career_losses(self) -> int:
        return sum(stint.losses for stint in self.coaching_stints.values())
