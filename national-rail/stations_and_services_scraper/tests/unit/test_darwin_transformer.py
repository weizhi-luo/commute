from data_model import Station, Service, ServiceStatus, Status, \
    CallingPoint, StationAndServices
from transform import DarwinStationAndServicesTransformer

import unittest
import pathlib
import json
from datetime import datetime
from os import path


TEST_DATA_FILE = path.join(
    str(pathlib.Path(__file__).parent.resolve()), 'test_data',
    'test_darwin_departure_board.json')


class TestTransform(unittest.TestCase):
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
        [CallingPoint('London Charing Cross', '13:35', False, '')], 10, '1')
    service_expected_2 = Service(
        '14etaXoW2Uyf34f3euTuUg==', ServiceStatus(Status.OnTime, ''),
        datetime.strptime('13:20', '%H:%M').time(),
        [CallingPoint('London Cannon Street', '13:41', False, '')], 8, '1')
    service_expected_3 = Service(
        '3ohw4h+KUjXfevFqr64amg==', ServiceStatus(Status.OnTime, ''),
        datetime.strptime('13:36', '%H:%M').time(),
        [CallingPoint('London Charing Cross', '14:05', False, '')], 10, '1')
    service_expected_4 = Service(
        'tao5H+0gvJKNM8g6EqbLPA==', ServiceStatus(Status.OnTime, ''),
        datetime.strptime('13:50', '%H:%M').time(),
        [CallingPoint('London Cannon Street', '14:11', False, '')], 10, '1')
    service_expected_5 = Service(
        'Ybb/0Pq05hK6WHCG7IVbtQ==', ServiceStatus(Status.OnTime, ''),
        datetime.strptime('14:06', '%H:%M').time(),
        [CallingPoint('London Charing Cross', '14:35', False, '')], 10)
    services_expected = [service_expected_1, service_expected_2,
                         service_expected_3, service_expected_4,
                         service_expected_5]

    @classmethod
    def setUpClass(cls):
        with open(TEST_DATA_FILE) as file:
            cls.departure_board = json.load(file)
        cls.station_and_services_expected = \
            StationAndServices(cls.station_expected, cls.services_expected)
        cls.transformer = DarwinStationAndServicesTransformer()

    def test_return_station_and_services_expected(self):
        station_and_services = self.transformer.transform(self.departure_board)
        self.assertEqual(station_and_services.station,
                         self.station_and_services_expected.station)

    def test_return_station_and_services_expected_1(self):
        station_and_services = self.transformer.transform(self.departure_board)
        services = self.station_and_services_expected.services
        self.assertSequenceEqual(station_and_services.services,
                         self.station_and_services_expected.services)


if __name__ == '__main__':
    unittest.main()
