import logging
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from s7_test.persistance.postgres_connection import PostgresConnector
from s7_test.persistance.bd_models import FlightModel


class Repository:
    def __init__(self, postgres: PostgresConnector):
        self.postgres = postgres

    async def write_to_db(self, model) -> None:
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

    async def get_flights_by_date(self, flight_date: date,) -> list:
        connection = await self.postgres.get_connection()
        async_session = sessionmaker(
            connection, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            try:
                async with session.begin():
                    row = await session.execute(
                        select(FlightModel).filter(
                            FlightModel.depdate == flight_date,
                        )
                    )
                    models = row.fetchall()
                    return models
            except Exception as ex:
                logging.error(f"Error selecting from db: {ex}")
