import datetime

from msgspec import Struct, field


class User(Struct, kw_only=True, dict=True):
    id: int
    username: str
    email: str
    password_hash: str
    created_at: datetime.datetime = field(default_factory=lambda : datetime.datetime.now(tz=datetime.UTC))
