from pytest import fixture

from s7_test.logic.file_processor import FileProcessor
from s7_test.persistance.postgres_connection import PostgresConnector
from s7_test.persistance.repository import Repository
from s7_test.scheduler.scheduler import Scheduler
from s7_test.scheduler.job_process_file import ProcessFileJob
from fake_settings import FakeSettings


@fixture()
def settings():
    return FakeSettings()


@fixture()
def postgres_connector(settings):
    return PostgresConnector(settings)


@fixture()
def repository(postgres_connector):
    return Repository(postgres_connector)


@fixture()
def file_processor(settings, repository):
    return FileProcessor(settings, repository)


@fixture()
def scheduler():
    return Scheduler()


@fixture()
def process_file_job(settings, file_processor):
    return ProcessFileJob(settings, file_processor)
