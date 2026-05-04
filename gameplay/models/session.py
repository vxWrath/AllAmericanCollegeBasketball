import datetime

from msgspec import Struct, field

__all__ = ["Session"]

class Session(Struct, kw_only=True, dict=True):
    id: int
    token: str
    user_id: int
    created_at: datetime.datetime = field(default_factory=lambda : datetime.datetime.now(tz=datetime.UTC))
    expires_at: datetime.datetime = field(default_factory=lambda : datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=7))
