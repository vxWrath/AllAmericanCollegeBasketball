import enum

from msgspec import Struct

__all__ = ["StatsScope", "PlayerStats"]


class StatsScope(enum.IntEnum):
    REGULAR_SEASON   = 0
    CONF_TOURNAMENT  = 1
    NCP_TOURNAMENT   = 2
    SCP_TOURNAMENT   = 3


class PlayerStats(Struct, kw_only=True, dict=True):
    id: int
    career_id: int
    player_id: int
    team_id: int
    season: int
    scope: StatsScope

    # Denormalized from Player for award queries (All-Conference by position, etc.)
    position: int  # Position enum value

    games_played: int = 0

    oreb: int = 0
    dreb: int = 0
    assists: int = 0
    steals: int = 0
    blocks: int = 0
    turnovers: int = 0

    fg_made: int = 0
    fg_attempts: int = 0
    three_made: int = 0
    three_attempts: int = 0
    ft_made: int = 0
    ft_attempts: int = 0

    # --- derived totals ---

    @property
    def two_made(self) -> int:
        return self.fg_made - self.three_made

    @property
    def two_attempts(self) -> int:
        return self.fg_attempts - self.three_attempts

    @property
    def points(self) -> int:
        return self.two_made * 2 + self.three_made * 3 + self.ft_made

    @property
    def rebounds(self) -> int:
        return self.oreb + self.dreb

    # --- per-game averages ---

    def _per_game(self, value: int) -> float:
        if self.games_played == 0:
            return 0.0
        return round(value / self.games_played, 1)

    @property
    def ppg(self) -> float:
        return self._per_game(self.points)

    @property
    def rpg(self) -> float:
        return self._per_game(self.rebounds)

    @property
    def apg(self) -> float:
        return self._per_game(self.assists)

    @property
    def spg(self) -> float:
        return self._per_game(self.steals)

    @property
    def bpg(self) -> float:
        return self._per_game(self.blocks)

    @property
    def topg(self) -> float:
        return self._per_game(self.turnovers)

    # --- shooting percentages ---

    @property
    def fg_pct(self) -> float | None:
        if self.fg_attempts == 0:
            return None
        return round(self.fg_made / self.fg_attempts, 3)

    @property
    def two_pct(self) -> float | None:
        if self.two_attempts == 0:
            return None
        return round(self.two_made / self.two_attempts, 3)

    @property
    def three_pct(self) -> float | None:
        if self.three_attempts == 0:
            return None
        return round(self.three_made / self.three_attempts, 3)

    @property
    def ft_pct(self) -> float | None:
        if self.ft_attempts == 0:
            return None
        return round(self.ft_made / self.ft_attempts, 3)
