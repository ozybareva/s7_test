import asyncio
import logging
import uvicorn
from fastapi import FastAPI

from logic.file_processor import FileProcessor
from persistance.postgres_connection import PostgresConnector
from persistance.repository import Repository
from scheduler.scheduler import Scheduler
from scheduler.job_process_file import ProcessFileJob
from settings import Settings

logging.basicConfig(level=logging.DEBUG)


class App:
    def __init__(self):
        logging.info("Initializing application")

        self.app = FastAPI()
        self.loop = asyncio.get_event_loop()
        self.settings = Settings()
        self.server = self.init_server(self.loop)
        self._postgres_connector = PostgresConnector(self.settings)
        self._repository = Repository(self._postgres_connector)
        self.file_processor = FileProcessor(self.settings, self._repository)
        self.scheduler = self._get_scheduler()

    def start(self):
        self.add_routes()

        try:
            logging.info("Start application")
            tasks = asyncio.gather(
                self.scheduler.schedule_task_periodically(),
                self.server.serve(),
            )
            self.loop.run_until_complete(tasks)

            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        except Exception:
            logging.error("Unexpected error")
        finally:
            self.loop.close()

    def init_server(self, loop):
        config = uvicorn.Config(app=self.app, loop=loop, host="0.0.0.0")

        return uvicorn.Server(config)

    def add_routes(self):
        self.app.add_api_route(
            "/get_flights", self._repository.get_flights_by_date, methods=["POST"]
        )

    def _get_scheduler(self) -> Scheduler:
        scheduler = Scheduler()
        process_file_job = ProcessFileJob(self.settings, self.file_processor)
        scheduler.register(process_file_job)
        return scheduler
