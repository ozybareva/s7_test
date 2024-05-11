from datetime import date
from pydantic import BaseModel


class FlightModel(BaseModel):
    file_name: str
    flt: int
    depdate: str
    dep: str


class FlightResponseModel(BaseModel):
    flights: list[FlightModel]
