from sqlalchemy import BigInteger, Float, ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    career_id: Mapped[int] = mapped_column(
        ForeignKey("careers.id", ondelete="CASCADE"),
        index=True,
    )

    conference: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    primary_color: Mapped[str] = mapped_column(String(7), nullable=False)  # hex color

    preseason_rating: Mapped[float] = mapped_column(Float, nullable=False)
    preseason_rank: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    current_rating: Mapped[float] = mapped_column(Float, nullable=False)
    previous_rating: Mapped[float] = mapped_column(Float, nullable=False)

    current_rank: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    previous_rank: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    accomplishments: Mapped[dict] = mapped_column(JSONB, nullable=False)
