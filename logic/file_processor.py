import csv
import json
import os
import shutil
import logging
from datetime import datetime
from pathlib import Path

from persistance.repository import Repository
from persistance.models import FlightModel
from settings import Settings


class FileProcessor:
    def __init__(self, settings: Settings, repository: Repository):
        self.input_folder = Path(f"{settings.path_to_folders}/In")
        self.output_folder = Path(f"{settings.path_to_folders}/Out")
        self.ok_folder = Path(f"{settings.path_to_folders}/Ok")
        self.repository = repository

    @staticmethod
    def format_dmy_date(d):
        modified_date = d[:2] + d[2:5].capitalize() + "19" + d[5:]
        return datetime.strptime(modified_date, "%d%b%Y").strftime("%Y-%m-%d")

    @staticmethod
    def format_ymd_date(d):
        return datetime.strptime(d, "%Y%m%d").strftime("%Y-%m-%d")

    async def parse_file(self, filename, result_json):
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

    async def process_flight_info(self):
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
            await self.repository.write_to_db(
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
