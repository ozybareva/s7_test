from pytest import fixture


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
        "prl": [{
            'bdate': '1973-11-11',
            'firstname': 'IVAN',
            'num': '1',
            'surname': 'IVANOV',
        }]}
