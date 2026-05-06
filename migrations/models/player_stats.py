from sqlalchemy import BigInteger, ForeignKey, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

__all__ = ["PlayerStats"]


class PlayerStats(Base):
    __tablename__ = "player_stats"

    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "season",
            "scope",
            name="uq_player_stats_player_season_scope",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    career_id: Mapped[int] = mapped_column(
        ForeignKey("careers.id", ondelete="CASCADE"),
        index=True,
    )
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"),
        index=True,
    )
    team_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    season: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    scope: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # StatsScope enum

    # Denormalized from Player for award queries (position-based All-Conference, etc.)
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # Position enum

    games_played: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    # points is computed (two_made*2 + three_made*3 + ft_made), not stored
    oreb: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    dreb: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    assists: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    steals: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    blocks: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    turnovers: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    fg_made: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    fg_attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    three_made: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    three_attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    ft_made: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    ft_attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False)
