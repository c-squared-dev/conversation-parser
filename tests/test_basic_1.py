import json
import csv

from conversation_parser_v2 import RapidProParser
from tests import testutils

import pytest


@pytest.fixture(scope='module')
def json_data():
    with open(testutils.resource_filename('basic_1.json')) as json_file:
        return json.load(json_file)


@pytest.fixture(scope='module')
def csv_path():
    return testutils.resource_filename('basic_1.csv')


class TestBasic1:

    def test_json_key_check(self, json_data: any):
        print('json_data: {0}'.format(json.dumps(
            json_data, indent=4, sort_keys=True)))
        assert "flows" in json_data

    def test_csv_column_check(self, csv_path):
        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file)
            print('fieldnames', reader.fieldnames)
            assert "row_id" in reader.fieldnames

    def test_csv_to_json(self):
        # Does not work as not setup to accept csv/json input args
        parser = RapidProParser()
        output = parser.run()
        print('output', output)
        assert False is True
