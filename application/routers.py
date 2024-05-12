import logging

from datetime import date
from fastapi.responses import JSONResponse
from logic.file_processor import FileProcessor


class FlightDataRouter:
    def __init__(self, file_processor: FileProcessor) -> None:
        self.file_processor = file_processor

    async def get_flights_by_date(
        self,
        flight_date: date = date.today(),
    ):
        try:
            flights = await self.file_processor.get_flights_by_date(flight_date)
            return JSONResponse(flights.dict())
        except Exception as exc:
            logging.error(f"Error {exc}")
            return JSONResponse({"Status": "Error"})
