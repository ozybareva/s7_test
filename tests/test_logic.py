import pytest
from fixtures import flight_data_json_before_parsing, flight_data_json_after_parsing


def test_get_flight_info_with_correct_filename(file_processor):
    flight_date, flight_number, airport_name = file_processor.get_flight_info(
        "20221129_1234_DME.csv"
    )
    assert flight_date == "20221129"
    assert flight_number == "1234"
    assert airport_name == "DME"


def test_get_flight_info_with_incorrect_filename(file_processor):
    with pytest.raises(ValueError):
        flight_date, flight_number, airport_name = file_processor.get_flight_info("2")


@pytest.mark.asyncio
async def test_process_flight_info(mocker, repository, file_processor):
    mocker.patch.object(
        file_processor, "get_flight_info", return_value=("20221129", "1234", "DME")
    )
    mocker.patch.object(repository, "write_to_db", return_value=None)
    move_input_file = mocker.patch.object(
        file_processor, "move_input_file", return_value=None
    )
    save_json_file = mocker.patch.object(
        file_processor, "save_json_file", return_value=None
    )
    await file_processor.process_flight_info()

    move_input_file.assert_called_with()
    save_json_file.assert_called_with()


@pytest.mark.asyncio
async def test_parse_flight_file(
    repository,
    file_processor,
    flight_data_json_before_parsing,
    flight_data_json_after_parsing,
):
    parse_file_result = await file_processor.parse_file(
        "20221129_1234_DME.csv", flight_data_json_before_parsing
    )
    assert parse_file_result == flight_data_json_after_parsing


@pytest.mark.asyncio
async def test_parse_empty_flight_file(
    repository,
    file_processor,
    flight_data_json_before_parsing,
    flight_data_json_after_parsing,
):
    parse_file_result = await file_processor.parse_file(
        "invalid_20221129_1234_DME.csv", flight_data_json_before_parsing
    )
    assert parse_file_result is None
