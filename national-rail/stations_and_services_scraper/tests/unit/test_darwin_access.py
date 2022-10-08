"""Unit tests for darwin_access and related functions"""
import unittest
import pathlib
import json
from unittest.mock import Mock, patch
from os import path
from datetime import datetime

from error import StationCrsCodeNotFoundError
from data_access.darwin.darwin_access import get_station_and_services,\
                                             DarwinDataAccess
from data_model import Service, ServiceStatus, Status, CallingPoint, Station,\
                       StationAndServices, OriginAndCallingPointNames
from config_access import ConfigAccess


TEST_DATA_FILE = path.join(
    str(pathlib.Path(__file__).parent.resolve()), 'test_data',
    'test_darwin_departure_board.json')


class TestGetStationAndServices(unittest.TestCase):
    station_expected = Station('Charlton', True,
                               ('\nA reduced service will operate on Southern,'
                                ' Thameslink and Great Northern routes until'
                                ' further notice. More information can be '
                                'found in <a href=\'http://nationalrail.co.uk/'
                                'service_disruptions/287384.aspx\'>Latest '
                                'Travel News</a>.\n<p>\nAll toilets at the '
                                'station are out of order at Charlton station.'
                                '</p>'))
    service_expected_1 = Service(
        'Ejj51DopLBG4oePJ8QS1vw==', ServiceStatus(Status.NewTime, ''),
        datetime.strptime('13:08', '%H:%M').time(),
        [CallingPoint('London Charing Cross', '13:35', False, '')])
    service_expected_1.set_length(10)
    service_expected_1.set_platform('1')
    service_expected_2 = Service(
        '14etaXoW2Uyf34f3euTuUg==', ServiceStatus(Status.OnTime, ''),
        datetime.strptime('13:20', '%H:%M').time(),
        [CallingPoint('London Cannon Street', '13:41', False, '')])
    service_expected_2.set_length(8)
    service_expected_2.set_platform('1')
    service_expected_3 = Service(
        '3ohw4h+KUjXfevFqr64amg==', ServiceStatus(Status.OnTime, ''),
        datetime.strptime('13:36', '%H:%M').time(),
        [CallingPoint('London Charing Cross', '14:05', False, '')])
    service_expected_3.set_length(10)
    service_expected_3.set_platform('1')
    service_expected_4 = Service(
        'tao5H+0gvJKNM8g6EqbLPA==', ServiceStatus(Status.OnTime, ''),
        datetime.strptime('13:50', '%H:%M').time(),
        [CallingPoint('London Cannon Street', '14:11', False, '')])
    service_expected_4.set_length(10)
    service_expected_4.set_platform('1')
    service_expected_5 = Service(
        'Ybb/0Pq05hK6WHCG7IVbtQ==', ServiceStatus(Status.OnTime, ''),
        datetime.strptime('14:06', '%H:%M').time(),
        [CallingPoint('London Charing Cross', '14:35', False, '')])
    service_expected_5.set_length(10)
    services_expected = [service_expected_1, service_expected_2,
                         service_expected_3, service_expected_4,
                         service_expected_5]

    @classmethod
    def setUpClass(cls):
        with open(TEST_DATA_FILE) as file:
            cls.departure_board = json.load(file)
        cls.calling_point_names_included = {
            'London Cannon Street', 'London Charing Cross'}
        cls.station_and_services_expected =\
            StationAndServices(cls.station_expected, cls.services_expected)

    def test_return_station_and_services(self):
        station_and_services = get_station_and_services(
            self.departure_board, self.calling_point_names_included)
        self.assertEqual(station_and_services,
                         self.station_and_services_expected)


class TestDarwinDataAccess(unittest.TestCase):
    origin = 'Charlton'
    calling_point_names = {'London Cannon Street'}
    error_message = f'Station crs code cannot be found for {origin}'

    @classmethod
    def setUpClass(cls) -> None:
        with open(TEST_DATA_FILE) as file:
            cls.departure_board = json.load(file)
        cls.config_setting = Mock(spec=ConfigAccess)
        cls.origin_and_calling_point_names = OriginAndCallingPointNames(
            cls.origin, cls.calling_point_names)
        cls.error = StationCrsCodeNotFoundError(cls.error_message)

    def test_darwin_client_get_departure_board_with_details_is_called(self):
        with patch('data_access.darwin.darwin_access.DarwinClient')\
                as mock_darwin_client:
            mock_darwin_client.get_departure_board_with_details\
                .return_value = None
            darwin_data_access = DarwinDataAccess(self.config_setting)
            darwin_data_access._client = mock_darwin_client
            with patch('data_access.darwin.darwin_access.'
                       'get_station_and_services')\
                    as mock_get_station_and_services:
                mock_get_station_and_services.return_value = None
                darwin_data_access.get_station_and_services(
                    self.origin_and_calling_point_names)
        mock_darwin_client.get_departure_board_with_details\
            .assert_called_with(self.origin)

    def test_darwin_client_get_departure_board_with_details_raises_error(self):
        with patch('data_access.darwin.darwin_access.DarwinClient')\
                as mock_darwin_client:
            mock_darwin_client._station_name_crs_code_mapping = {}
            mock_darwin_client.get_departure_board_with_details\
                .side_effect = self.error
            darwin_data_access = DarwinDataAccess(self.config_setting)
            darwin_data_access._client = mock_darwin_client
            with self.assertRaises(StationCrsCodeNotFoundError) as context:
                darwin_data_access.get_station_and_services(
                    self.origin_and_calling_point_names)
        self.assertTrue(self.error_message in str(context.exception))

    def test_get_departure_board_with_details_is_called(self):
        with patch('data_access.darwin.darwin_access.DarwinClient')\
                as mock_darwin_client:
            mock_darwin_client.get_departure_board_with_details\
                .return_value = self.departure_board
            darwin_data_access = DarwinDataAccess(self.config_setting)
            darwin_data_access._client = mock_darwin_client
            with patch('data_access.darwin.darwin_access.'
                       'get_station_and_services')\
                    as mock_get_station_and_services:
                mock_get_station_and_services.return_value = None
                darwin_data_access.get_station_and_services(
                    self.origin_and_calling_point_names)
        mock_get_station_and_services.assert_called_with(
            self.departure_board, self.calling_point_names)
