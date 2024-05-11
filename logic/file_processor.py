import csv
import json
import os
import shutil
import logging
from datetime import datetime, date
from pathlib import Path

from persistance.repository import Repository
from application.api_models import FlightResponseModel, FlightModel
from settings import Settings


class FileProcessor:
    def __init__(self, settings: Settings, repository: Repository):
        self.input_folder = Path(f"{settings.path_to_folders}/In")
        self.output_folder = Path(f"{settings.path_to_folders}/Out")
        self.ok_folder = Path(f"{settings.path_to_folders}/Ok")
        self._repository = repository

    @staticmethod
    def format_dmy_date(d) -> str:
        modified_date = d[:2] + d[2:5].capitalize() + "19" + d[5:]
        return datetime.strptime(modified_date, "%d%b%Y").strftime("%Y-%m-%d")

    @staticmethod
    def format_ymd_date(d) -> str:
        return datetime.strptime(d, "%Y%m%d").strftime("%Y-%m-%d")

    async def parse_file(self, filename, result_json) -> dict:
        try:
            with open(f"{self.input_folder}/{filename}") as file:
                reader = csv.reader(file, delimiter=";", quotechar="|")
                next(reader)
                for row in reader:
                    person = {
                        "num": row[0],
                        "surname": row[1],
                        "firstname": row[2],
                        "bdate": self.format_dmy_date(row[3]),
                    }
                    result_json["prl"].append(person)
                logging.info(f"File {filename} was parsed successfully")
            return result_json
        except Exception as ex:
            logging.error(f"Parsing error: {ex}")

    @staticmethod
    def get_flight_info(filename):
        return filename[:-4].split("_")

    async def process_flight_info(self) -> None:
        logging.info("Start processing flight info")

        for filename in os.listdir(self.input_folder):
            flight_date, flight_number, airport_name = self.get_flight_info(filename)
            flight_date = self.format_ymd_date(flight_date)
            result_json = {
                "flt": flight_number,
                "date": flight_date,
                "dep": airport_name,
                "prl": [],
            }
            await self._repository.write_to_db(
                FlightModel(
                    file_name=filename,
                    flt=int(flight_number),
                    depdate=datetime.strptime(flight_date, "%Y-%m-%d"),
                    dep=airport_name,
                )
            )

            file_data = await self.parse_file(filename, result_json)

            with open(f"{self.output_folder}/{filename[:-4]}.json", "w") as file:
                json.dump(file_data, file)
            logging.info(f"Json file for {filename} saved to {self.output_folder}")

            shutil.move(
                f"{self.input_folder}/{filename}", f"{self.ok_folder}/{filename}"
            )
            logging.info(f"File {filename} moved to {self.ok_folder}")

    async def get_flights_by_date(
        self, start_date: date, end_date: date
    ) -> FlightResponseModel:
        flight_models = await self._repository.get_flights_by_date(start_date, end_date)
        flight_response = FlightResponseModel(
            flights=[
                FlightModel(
                    file_name=model[0].file_name,
                    flt=model[0].flt,
                    depdate=model[0].depdate.strftime("%Y-/%m/-%d"),
                    dep=model[0].dep,
                )
                for model in flight_models
            ]
        )
        return flight_response
