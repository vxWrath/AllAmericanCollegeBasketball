
from sqlalchemy import (
    BigInteger,
    Boolean,
    Float,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

__all__ = ["Player", "Recruit"]

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    career_id: Mapped[int] = mapped_column(
        ForeignKey("careers.id", ondelete="CASCADE"),
        index=True,
    )
    team_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # Position enum
    year: Mapped[int] = mapped_column(SmallInteger, nullable=False)      # Year enum
    origin: Mapped[str] = mapped_column(String(50), nullable=False)      # PlayerOrigin enum

    inside_shot: Mapped[float] = mapped_column(Float, nullable=False)
    outside_shot: Mapped[float] = mapped_column(Float, nullable=False)
    interior_defense: Mapped[float] = mapped_column(Float, nullable=False)
    perimeter_defense: Mapped[float] = mapped_column(Float, nullable=False)
    athleticism: Mapped[float] = mapped_column(Float, nullable=False)
    playmaking: Mapped[float] = mapped_column(Float, nullable=False)

    dev_rate: Mapped[float] = mapped_column(Float, nullable=False)
    games_played: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    is_transferring: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Recruit(Base):
    __tablename__ = "recruits"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    career_id: Mapped[int] = mapped_column(
        ForeignKey("careers.id", ondelete="CASCADE"),
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # Position enum
    origin: Mapped[str] = mapped_column(String(50), nullable=False)      # PlayerOrigin enum
    estimated_stars: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    dev_rate: Mapped[float] = mapped_column(Float, nullable=False)

    inside_shot: Mapped[float] = mapped_column(Float, nullable=False)
    outside_shot: Mapped[float] = mapped_column(Float, nullable=False)
    interior_defense: Mapped[float] = mapped_column(Float, nullable=False)
    perimeter_defense: Mapped[float] = mapped_column(Float, nullable=False)
    athleticism: Mapped[float] = mapped_column(Float, nullable=False)
    playmaking: Mapped[float] = mapped_column(Float, nullable=False)

    scouted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    committed_to: Mapped[int | None] = mapped_column(Integer, nullable=True)
