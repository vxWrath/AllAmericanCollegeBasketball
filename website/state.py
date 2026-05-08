from blacksheep import Application
from blacksheep.client.session import ClientSession

from services import Cache, Database

__all__ = ["State"]


class State:
    app: Application
    cache: Cache
    database: Database
    session: ClientSession

    def __init__(self) -> None:
        self.cache = Cache(None)
        self.database = Database(self.cache)
        self.session = ClientSession()

    def set_app(self, app: Application) -> None:
        self.app = app

    async def connect(self) -> None:
        await self.cache.connect()
        await self.database.connect()
        await self.session.__aenter__()

    async def close(self) -> None:
        await self.database.close()
        await self.cache.close()
        await self.session.__aexit__(None, None, None)
