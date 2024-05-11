from pytest import fixture

from persistance.postgres_connection import PostgresConnector
from tests.settings import FakeSettings


@fixture()
def settings():
    return FakeSettings


@fixture()
def postgres_connector(settings):
    return PostgresConnector(settings)