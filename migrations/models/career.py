import datetime

from sqlalchemy import TIMESTAMP, BigInteger, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Career(Base):
    __tablename__ = "careers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    last_played_at: Mapped[datetime.datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    coach_name: Mapped[str] = mapped_column(String(100), nullable=False)
    rng_seed: Mapped[int] = mapped_column(Integer, nullable=False)
    current_season: Mapped[int] = mapped_column(Integer, nullable=False)
    current_week: Mapped[int] = mapped_column(Integer, nullable=False)
    current_team_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    coaching_stints: Mapped[dict] = mapped_column(JSONB, nullable=False)
