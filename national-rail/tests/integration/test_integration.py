"""Integration test"""
import os
import unittest
import pathlib
import json
import filecmp
from os import path

from data_access import DataAccess
from data_scrape import scrape_stations_and_services
from data_access.darwin.darwin_access import get_station_and_services
from data_model import OriginAndCallingPointNames, StationAndServices
from data_publish import publish
from data_publish.serialize import JsonDataSerializer
from data_publish.publish import DataPublisher


TEST_DATA_FILE = path.join(
    str(pathlib.Path(__file__).parent.resolve()), 'test_data',
    'test_darwin_departure_board.json')
EXPECTED_TEST_RESULTS_FILE = path.join(
    str(pathlib.Path(__file__).parent.resolve()), 'test_results',
    'expected_results.json')
TEST_RESULTS_FILE = path.join(
    str(pathlib.Path(__file__).parent.resolve()), 'test_results',
    'results.json')


class StubDataAccess(DataAccess):
    def get_station_and_services(
            self, origin_and_calling_point_names: OriginAndCallingPointNames)\
            -> StationAndServices:
        with open(TEST_DATA_FILE) as file:
            departure_board = json.load(file)
        return get_station_and_services(
            departure_board, {'London Charing Cross', 'London Cannon Street'})


class FakeDataPublisher(DataPublisher):
    def __init__(self, serializer):
        self._serializer = serializer

    def publish(self, data: object) -> None:
        serialized_data = self._serializer.serialize(data)
        with open(TEST_RESULTS_FILE, 'w') as f:
            f.write(serialized_data)


class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if path.exists(TEST_RESULTS_FILE):
            os.remove(TEST_RESULTS_FILE)

    def test_scrape_and_publish(self):
        data_access = StubDataAccess()
        data_publisher = FakeDataPublisher(JsonDataSerializer())

        station_and_services = scrape_stations_and_services(
            data_access, [OriginAndCallingPointNames('Test', {'Test'})])
        publish(data_publisher, station_and_services)

        assert filecmp.cmp(TEST_RESULTS_FILE, EXPECTED_TEST_RESULTS_FILE)
