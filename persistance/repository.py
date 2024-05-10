import logging
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from persistance.postgres_connection import PostgresConnector
from persistance.models import FlightModel


class Repository:
    def __init__(self, postgres: PostgresConnector):
        self.postgres = postgres

    async def write_to_db(self, model):
        connection = await self.postgres.get_connection()
        async_session = sessionmaker(
            connection, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            try:
                async with session.begin():
                    session.add(model)
                    await session.commit()
                logging.info("File info saved to db")
            except Exception as ex:
                logging.error(f"Error writing to db: {ex}")

    async def get_flights_by_date(
        self, start_date: date = date.today(), end_date: date = date.today()
    ):
        connection = await self.postgres.get_connection()
        async_session = sessionmaker(
            connection, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            try:
                async with session.begin():
                    row = await session.execute(
                        select(FlightModel).filter(
                            FlightModel.depdate >= start_date,
                            FlightModel.depdate <= end_date,
                        )
                    )
                    models = row.fetchone()
                    return models[0]
            except Exception as ex:
                logging.error(f"Error selecting from db: {ex}")
