from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import database_exists, create_database

from persistance.models import Base

from settings import Settings


class PostgresConnector:
    def __init__(self, settings: Settings):
        self.postgres_dsn = settings.postgres_dsn
        self.connection = None
        self.session = None

    async def get_connection(self):
        if not self.connection:
            self.connection = create_async_engine(self.postgres_dsn)
        return self.connection

    async def declare_base(self):
        engine = await self.get_connection()
        if not database_exists(engine.url):
            create_database(engine.url)
        Base.metadata.create_all(engine)
        return Base
