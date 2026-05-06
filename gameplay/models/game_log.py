import math
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

    def is_win(self) -> bool:
        return self.team_score > self.opponent_score

    def been_played(self) -> bool:
        return self.team_score > 0 or self.opponent_score > 0

    def margin(self) -> int:
        """Return margin from this team's perspective (positive = win margin)"""
        return self.team_score - self.opponent_score

    def is_close_game(self, threshold: int = 5) -> bool:
        """Return True if game was decided by threshold or fewer points"""
        return abs(self.margin()) <= threshold

    def is_blowout(self, threshold: int = 15) -> bool:
        """Return True if game was decided by more than threshold points"""
        return abs(self.margin()) > threshold

    def is_home(self) -> bool:
        return self.location == GameLocation.HOME

    def is_away(self) -> bool:
        return self.location == GameLocation.AWAY

    def is_conf(self) -> bool:
        return self.type == GameType.CONFERENCE

    def is_nonconf(self) -> bool:
        return self.type == GameType.NON_CONFERENCE

    def is_conf_tournament(self) -> bool:
        return self.type == GameType.CONF_TOURNAMENT

    def is_nc_tournament(self) -> bool:
        return self.type == GameType.NCP_TOURNAMENT

    def is_sc_tournament(self) -> bool:
        return self.type == GameType.SCP_TOURNAMENT

    def expected_margin(self) -> int:
        # Use live internal ratings when available (stamped just before game simulation).
        # Divide by 20 to normalize the ~30-130 rating scale back to the ~0-10 overall
        # scale so the tanh constants remain well-calibrated.
        # Fall back to static roster overall when live ratings are not yet set.
        if not self.team_rating_at_time or not self.opponent_rating_at_time:
            raise ValueError("Live ratings not set for this game log entry")

        if self.team_rating_at_time > 0 and self.opponent_rating_at_time > 0:
            rating_diff = (self.team_rating_at_time - self.opponent_rating_at_time) / 20.0
        else:
            rating_diff = self.team_overall - self.opponent_overall

        # Map rating difference to a raw margin, then compress with tanh to cap blowouts.
        raw_margin = rating_diff * 14.5
        margin = 55 * math.tanh(raw_margin / 55)

        # Fixed home-court advantage (~3.5 pts is the college basketball consensus).
        if self.is_home():
            margin += 3.5
        elif self.is_away():
            margin -= 3.5

        # Tiny tiebreaker nudge toward the favored side (handles exact-even neutral games).
        if rating_diff > 0:
            margin += 0.5
        elif rating_diff < 0:
            margin -= 0.5

        return round(margin)
