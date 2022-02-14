"""Unit tests for get_station and related functions"""
import unittest

from data_model import Station
from data_access.darwin.station import get_station, get_departure_board_message


class TestGetDepartureBoardMessage(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original_message_1 = (
            '\nA reduced service will operate on Southern, Thameslink and '
            'Great Northern routes until further notice. More information can '
            'be found in <a href="http://nationalrail.co.uk/service_'
            'disruptions/287384.aspx">Latest Travel News</a>.')
        cls.original_message_2 = (
            '<p>\nAll toilets at the station are out of '
            'order at Charlton station.</p>')
        cls.original_message_3 = 'No services'

    def test_none_message_return_empty_message(self):
        departure_board = {'nrccMessages': None}
        message = get_departure_board_message(departure_board)
        message_expected = ''

        self.assertEqual(message, message_expected)

    def test_empty_message_return_empty_message(self):
        departure_board = {'nrccMessages': {'message': []}}
        message = get_departure_board_message(departure_board)
        message_expected = ''

        self.assertEqual(message, message_expected)

    def test_one_messages_return_message(self):
        departure_board = {
            'nrccMessages': {
                'message': [{'_value_1': self.original_message_3}]
            }
        }
        message = get_departure_board_message(departure_board)
        message_expected = self.original_message_3

        self.assertEqual(message, message_expected)

    def test_two_messages_return_message(self):
        departure_board = {
            'nrccMessages': {
                'message': [{'_value_1': self.original_message_1},
                            {'_value_1': self.original_message_2}]
            }
        }
        message = get_departure_board_message(departure_board)
        message_expected = \
            '\n'.join((self.original_message_1, self.original_message_2))

        self.assertEqual(message, message_expected)


class TestGetStation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original_message_1 = (
            '\nA reduced service will operate on Southern, Thameslink and '
            'Great Northern routes until further notice. More information can '
            'be found in <a href="http://nationalrail.co.uk/service_'
            'disruptions/287384.aspx">Latest Travel News</a>.')
        cls.original_message_2 = (
            '<p>\nAll toilets at the station are out of '
            'order at Charlton station.</p>')
        cls.original_message_3 = 'No services'

    def test_get_station_with_message(self):
        departure_board = {
            'locationName': 'Charlton',
            'areServicesAvailable': None,
            'nrccMessages': {
                'message': [{'_value_1': self.original_message_1},
                            {'_value_1': self.original_message_2}]
            }
        }
        station = get_station(departure_board)
        station_expected = Station(
            'Charlton', True, '\n'.join([self.original_message_1,
                                         self.original_message_2])
        )

        self.assertEqual(station, station_expected)

    def test_get_station_with_no_services(self):
        departure_board = {
            'locationName': 'Blackheath',
            'areServicesAvailable': False,
            'nrccMessages': {
                'message': [{'_value_1': self.original_message_3}]
            }
        }
        station = get_station(departure_board)
        station_expected = Station(
            'Blackheath', False, self.original_message_3)

        self.assertEqual(station, station_expected)

    def test_get_station_with_no_services_messages(self):
        departure_board = {
            'locationName': 'Blackheath',
            'areServicesAvailable': False,
            'nrccMessages': None
        }
        station = get_station(departure_board)
        station_expected = Station('Blackheath', False, '')

        self.assertEqual(station, station_expected)
