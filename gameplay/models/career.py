import datetime
from typing import Self

from msgspec import Struct, field


class Career(Struct, kw_only=True, dict=True):
    id: int
    user_id: int
    created_at: datetime.datetime = field(default_factory=lambda : datetime.datetime.now(tz=datetime.UTC))
    last_played_at: datetime.datetime | None = None

    def update_last_played_at(self) -> Self:
        self.last_played_at = datetime.datetime.now(tz=datetime.UTC)
        return self
