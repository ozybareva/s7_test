from sqlalchemy import Column, Integer, Date, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class FlightPostgresModel(Base):
    __tablename__ = "flight"
    id = Column(Integer, primary_key=True)
    file_name = Column("file_name", Text)
    flt = Column("flt", Integer)
    depdate = Column("depdate", Date)
    dep = Column("dep", Text)
