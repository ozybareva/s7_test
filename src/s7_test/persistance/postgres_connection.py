import logging
import asyncpg
from asyncpg.exceptions import InvalidCatalogNameError

from sqlalchemy.ext.asyncio import create_async_engine

from s7_test.persistance.bd_models import Base

from s7_test.settings import Settings


class PostgresConnector:
    def __init__(self, settings: Settings):
        self.postgres_dsn = settings.postgres_dsn
        self.postgres_user = settings.postgres_user
        self.postgres_db = settings.postgres_db
        self.connection = None
        self.session = None

    async def get_connection(self):
        if not self.connection:
            self.connection = create_async_engine(
                f"{self.postgres_dsn}/{self.postgres_db}"
            )
        return self.connection

    async def declare_base(self) -> None:
        try:
            await asyncpg.connect(user=self.postgres_user, database=self.postgres_db)
        except InvalidCatalogNameError:
            sys_conn = await asyncpg.connect(database="postgres", user="postgres")
            await sys_conn.execute(
                f'CREATE DATABASE "{self.postgres_db}" OWNER "{self.postgres_user}"'
            )
            await sys_conn.close()
            logging.info("Database created")
        await self.create_table()

    async def create_table(self):
        engine = await self.get_connection()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logging.info("Tables created")

    async def run_startup(self) -> None:
        await self.declare_base()

    async def run_shutdown(self) -> None:
        if self.connection:
            await self.connection.dispose()
