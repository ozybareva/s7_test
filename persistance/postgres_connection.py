import logging

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
        async with engine.begin() as conn:
            if not conn.run_sync(database_exists, engine.url):
                await conn.run_sync(create_database(engine.url))
                logging.info("Database created")
            await conn.run_sync(Base.metadata.create_all)

    async def run_startup(self) -> None:
        await self.declare_base()

    async def run_shutdown(self) -> None:
        if self.connection:
            await self.connection.dispose()
