import asyncio
import logging
import uvicorn
from fastapi import FastAPI

from s7_test.application.routers import FlightDataRouter
from s7_test.logic.file_processor import FileProcessor
from s7_test.persistance.postgres_connection import PostgresConnector
from s7_test.persistance.repository import Repository
from s7_test.scheduler.scheduler import Scheduler
from s7_test.scheduler.job_process_file import ProcessFileJob
from s7_test.settings import Settings

logging.basicConfig(level=logging.DEBUG)


class App:
    def __init__(self):
        logging.info("Initializing application")

        self.app = FastAPI()
        self._loop = asyncio.get_event_loop()
        self.settings = Settings()
        self._server = self.init_server(self._loop)
        self._postgres_connector = PostgresConnector(self.settings)
        self._repository = Repository(self._postgres_connector)
        self._file_processor = FileProcessor(self.settings, self._repository)
        self._scheduler = self._get_scheduler()
        self._router = FlightDataRouter(self._file_processor)

    def start(self):
        self.add_routes()

        try:
            logging.info("Start application")
            self._loop.run_until_complete(self._postgres_connector.run_startup())
            tasks = asyncio.gather(
                self._scheduler.schedule_task_periodically(),
                self._server.serve(),
            )
            self._loop.run_until_complete(tasks)

            self._loop.run_forever()
        except KeyboardInterrupt:
            pass
        except Exception as ex:
            logging.error(f"Unexpected error: {ex}")
        finally:
            self._loop.run_until_complete(self._postgres_connector.run_shutdown())
            self._loop.close()

    def init_server(self, loop):
        config = uvicorn.Config(app=self.app, loop=loop, host="0.0.0.0")
        return uvicorn.Server(config)

    def add_routes(self) -> None:
        self.app.add_api_route(
            "/get_flights", self._router.get_flights_by_date, methods=["POST"]
        )

    def _get_scheduler(self) -> Scheduler:
        scheduler = Scheduler()
        process_file_job = ProcessFileJob(self.settings, self._file_processor)
        scheduler.register(process_file_job)
        return scheduler
