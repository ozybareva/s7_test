from application.routers import FlightDataRouter


def test_valid_request():
    assert FlightDataRouter()