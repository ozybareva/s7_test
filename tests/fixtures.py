from pytest import fixture
from datetime import date
from s7_test.persistance.bd_models import FlightPostgresModel
from fastapi.responses import JSONResponse


@fixture()
def flight_data_json_before_parsing():
    return {
        "flt": "flight_number",
        "date": "flight_date",
        "dep": "airport_name",
        "prl": [],
    }


@fixture()
def flight_data_json_after_parsing():
    return {
        "flt": "flight_number",
        "date": "flight_date",
        "dep": "airport_name",
        "prl": [
            {
                "bdate": "1973-11-11",
                "firstname": "IVAN",
                "num": "1",
                "surname": "IVANOV",
            }
        ],
    }


@fixture()
def request_date():
    return date(2022, 11, 29)


@fixture()
def flight_models():
    return [
        (
            FlightPostgresModel(
                id=1,
                file_name="test_filename_1",
                flt=1,
                depdate=date(2022, 11, 29),
                dep="test_airport_1",
            ),
        ),
        (
            FlightPostgresModel(
                id=2,
                file_name="test_filename_2",
                flt=2,
                depdate=date(2022, 11, 29),
                dep="test_airport_2",
            ),
        ),
    ]


@fixture()
def api_response_flight_models():
    return JSONResponse(
        {
            "flights": [
                {
                    "file_name": "test_filename_1",
                    "flt": 1,
                    "depdate": "2022-11-29",
                    "dep": "test_airport_1",
                },
                {
                    "file_name": "test_filename_2",
                    "flt": 2,
                    "depdate": "2022-11-29",
                    "dep": "test_airport_2",
                },
            ]
        }
    )


@fixture()
def response_error():
    return JSONResponse({"Status": "Error"})
