import pytest
from fixtures import (
    request_date,
    flight_models,
    api_response_flight_models,
    response_error,
)


@pytest.mark.asyncio
async def test_valid_request(
    flight_data_router,
    request_date,
    mocker,
    repository,
    flight_models,
    api_response_flight_models,
):
    mocker.patch.object(repository, "get_flights_by_date", return_value=flight_models)
    response = await flight_data_router.get_flights_by_date(request_date)
    assert response.body == api_response_flight_models.body


@pytest.mark.asyncio
async def test_error_response(
    flight_data_router, request_date, mocker, repository, response_error
):
    mocker.patch.object(repository, "get_flights_by_date", return_value=ValueError)
    response = await flight_data_router.get_flights_by_date(request_date)
    assert response.body == response_error.body
