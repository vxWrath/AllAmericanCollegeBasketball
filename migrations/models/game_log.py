
from sqlalchemy import BigInteger, Float, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class GameLog(Base):
    __tablename__ = "game_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    career_id: Mapped[int] = mapped_column(
        ForeignKey("careers.id", ondelete="CASCADE"),
        index=True,
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"),
        index=True,
    )

    week: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    opponent_team_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    location: Mapped[int] = mapped_column(SmallInteger, nullable=False)   # GameLocation enum
    type: Mapped[int] = mapped_column(SmallInteger, nullable=False)        # GameType enum

    team_overall: Mapped[float] = mapped_column(Float(precision=24), nullable=False)
    opponent_overall: Mapped[float] = mapped_column(Float(precision=24), nullable=False)

    team_score: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    opponent_score: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    overtimes: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    team_rank_at_time: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    opponent_rank_at_time: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    team_rating_at_time: Mapped[float | None] = mapped_column(Float(precision=24), nullable=True)
    opponent_rating_at_time: Mapped[float | None] = mapped_column(Float(precision=24), nullable=True)
