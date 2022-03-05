"""Unit tests for get_service and related functions"""
import unittest
from datetime import datetime

from data_model import Status, ServiceStatus, CallingPoint, Service
from data_access.darwin.service \
    import get_status, is_service_on_time, is_service_cancelled,\
    is_service_delayed, get_abnormality_message, get_service_status,\
    get_service_time, get_calling_point_time, is_calling_point_cancelled,\
    get_calling_point_alert, get_calling_point, get_calling_points,\
    get_service, is_valid_service, get_services


class TestIsServiceOnTime(unittest.TestCase):
    def test_on_time(self):
        service_item = {'etd': 'On time'}

        self.assertTrue(is_service_on_time(service_item))

    def test_not_on_time(self):
        service_item = {'etd': '00:15'}

        self.assertFalse(is_service_on_time(service_item))


class TestIsServiceCancelled(unittest.TestCase):
    def test_etd_set_to_On_time_isCancelled_not_set_to_True_is_not_cancelled(self):
        service_item = {'etd': 'On time', 'isCancelled': None}

        self.assertFalse(is_service_cancelled(service_item))

    def test_etd_set_to_Delayed_isCancelled_not_set_to_True_is_not_cancelled(self):
        service_item = {'etd': 'Delayed', 'isCancelled': None}

        self.assertFalse(is_service_cancelled(service_item))

    def test_etd_set_to_time_isCancelled_not_set_to_True_is_not_cancelled(self):
        service_item = {'etd': '09:41', 'isCancelled': None}

        self.assertFalse(is_service_cancelled(service_item))

    def test_etd_set_to_Cancelled_is_cancelled(self):
        service_item = {'etd': 'Cancelled'}

        self.assertTrue(is_service_cancelled(service_item))

    def test_isCancelled_set_to_True_etd_set_to_Cancelled_is_cancelled(self):
        service_item = {'etd': 'Cancelled', 'isCancelled': True}

        self.assertTrue(is_service_cancelled(service_item))

    def test_isCancelled_set_to_None_etd_set_to_Cancelled_is_cancelled(self):
        service_item = {'etd': 'Cancelled', 'isCancelled': None}

        self.assertTrue(is_service_cancelled(service_item))


class TestIsServiceDelayed(unittest.TestCase):
    def test_etd_set_to_On_time_isCancelled_not_set_to_True_is_not_delayed(self):
        service_item = {'std': '09:25', 'etd': 'On time', 'isCancelled': None}

        self.assertFalse(is_service_delayed(service_item))

    def test_etd_set_to_Delayed_isCancelled_not_set_to_True_is_delayed(self):
        service_item = {'std': '09:08', 'etd': 'Delayed', 'isCancelled': None}

        self.assertTrue(is_service_delayed(service_item))

    def test_etd_set_to_time_isCancelled_not_set_to_True_is_not_delayed(self):
        service_item = {'std': '09:40', 'etd': '09:41', 'isCancelled': None}

        self.assertFalse(is_service_delayed(service_item))

    def test_etd_set_to_Cancelled_is_note_delayed(self):
        service_item = {'etd': 'Cancelled'}

        self.assertFalse(is_service_delayed(service_item))

    def test_isCancelled_set_to_True_etd_set_to_Cancelled_is_not_delayed(self):
        service_item = {'etd': 'Cancelled', 'isCancelled': True}

        self.assertFalse(is_service_delayed(service_item))

    def test_isCancelled_set_to_None_etd_set_to_Cancelled_is_not_delayed(self):
        service_item = {'etd': 'Cancelled', 'isCancelled': None}

        self.assertFalse(is_service_delayed(service_item))


class TestGetAbnormalityMessage(unittest.TestCase):
    cancel_reason = 'Cancelled due to faulty train.'
    delay_reason = 'Delayed due to signalling problems.'
    adhoc_alerts = ['Toilets are unavailable.',
                    'Doors are not working at first carriage.']

    @classmethod
    def setUpClass(cls) -> None:
        cls.cancel_message = f'Cancel reason: {cls.cancel_reason}'
        cls.delay_message = f'Delay reason: {cls.delay_reason}'
        cls.adhoc_alerts_message = 'Alerts:\n' + '\n'.join(cls.adhoc_alerts)

    def test_return_cancel_message(self):
        service_item = {'cancelReason': self.cancel_reason,
                        'delayReason': None,
                        'adhocAlerts': None}
        message = get_abnormality_message(service_item)

        self.assertEqual(message, self.cancel_message)

    def test_return_delay_message(self):
        service_item = {'cancelReason': None,
                        'delayReason': self.delay_reason,
                        'adhocAlerts': None}
        message = get_abnormality_message(service_item)

        self.assertEqual(message, self.delay_message)

    def test_return_adhoc_alerts_message(self):
        service_item = {'cancelReason': None,
                        'delayReason': None,
                        'adhocAlerts': self.adhoc_alerts}
        message = get_abnormality_message(service_item)

        self.assertEqual(message, self.adhoc_alerts_message)

    def test_return_cancel_delay_messages(self):
        service_item = {'cancelReason': self.cancel_reason,
                        'delayReason': self.delay_reason,
                        'adhocAlerts': None}
        message = get_abnormality_message(service_item)
        message_expected = '\n'.join([self.cancel_message, self.delay_message])

        self.assertEqual(message, message_expected)

    def test_return_cancel_delay_adhoc_alerts_messages(self):
        service_item = {'cancelReason': self.cancel_reason,
                        'delayReason': self.delay_reason,
                        'adhocAlerts': self.adhoc_alerts}
        message = get_abnormality_message(service_item)
        message_expected = '\n'.join((self.cancel_message, self.delay_message,
                                      self.adhoc_alerts_message))
        self.assertEqual(message, message_expected)

    def test_return_cancel_adhoc_alerts_messages(self):
        service_item = {'cancelReason': self.cancel_reason,
                        'delayReason': None,
                        'adhocAlerts': self.adhoc_alerts}
        message = get_abnormality_message(service_item)
        message_expected = '\n'.join((self.cancel_message,
                                      self.adhoc_alerts_message))

        self.assertEqual(message, message_expected)

    def test_return_delay_adhoc_alerts_messages(self):
        service_item = {'cancelReason': None,
                        'delayReason': self.delay_reason,
                        'adhocAlerts': self.adhoc_alerts}
        message = get_abnormality_message(service_item)
        message_expected = '\n'.join((self.delay_message,
                                      self.adhoc_alerts_message))

        self.assertEqual(message, message_expected)

    def test_return_empty_message(self):
        service_item = {'cancelReason': None,
                        'delayReason': None,
                        'adhocAlerts': None}
        message = get_abnormality_message(service_item)

        self.assertEqual(message, '')


class TestGetStatus(unittest.TestCase):
    def test_etd_set_to_On_time_isCancelled_not_set_return_on_time(self):
        service_item = {'etd': 'On time', 'isCancelled': None}

        self.assertIs(get_status(service_item), Status.OnTime)

    def test_etd_set_to_time_isCancelled_not_set_return_new_time(self):
        service_item = {'etd': '00:15', 'isCancelled': None}

        self.assertIs(get_status(service_item), Status.NewTime)

    def test_etd_set_to_Delayed_isCancelled_not_set_return_delayed(self):
        service_item = {'etd': 'Delayed', 'isCancelled': None}

        self.assertIs(get_status(service_item), Status.Delayed)

    def test_etd_set_to_On_time_isCancelled_set_to_True_return_cancelled(self):
        service_item = {'etd': 'On time', 'isCancelled': True}

        self.assertIs(get_status(service_item), Status.Cancelled)

    def test_etd_set_to_time_isCancelled_set_to_True_return_cancelled(self):
        service_item = {'etd': '00:15', 'isCancelled': True}

        self.assertIs(get_status(service_item), Status.Cancelled)

    def test_etd_set_to_Cancelled_isCancelled_set_to_True_return_cancelled(self):
        service_item = {'etd': 'Cancelled', 'isCancelled': True}

        self.assertIs(get_status(service_item), Status.Cancelled)


class TestGetServiceStatus(unittest.TestCase):
    def test_return_on_time_service_status(self):
        service_item = {
            'etd': 'On time',
            'isCancelled': None,
            'cancelReason': None,
            'delayReason': None,
            'adhocAlerts': None
        }
        service_status = get_service_status(service_item)
        service_status_expected = ServiceStatus(Status.OnTime, '')

        self.assertEqual(service_status, service_status_expected)

    def test_return_cancelled_service_status(self):
        service_item = {
            'etd': 'Cancelled',
            'isCancelled': True,
            'cancelReason': 'Cancelled due to faulty train.',
            'delayReason': None,
            'adhocAlerts': None
        }
        service_status = get_service_status(service_item)
        service_status_expected =\
            ServiceStatus(Status.Cancelled,
                          'Cancel reason: Cancelled due to faulty train.')

        self.assertEqual(service_status, service_status_expected)

    def test_return_new_time_service_status(self):
        service_item = {
            'etd': '00:15',
            'isCancelled': None,
            'cancelReason': None,
            'delayReason': 'Delayed due to signalling problems.',
            'adhocAlerts': None
        }
        service_status = get_service_status(service_item)
        service_status_expected =\
            ServiceStatus(Status.NewTime,
                          'Delay reason: Delayed due to signalling problems.')

        self.assertEqual(service_status, service_status_expected)

    def test_return_delayed_service_status(self):
        service_item = {
            'etd': 'Delayed',
            'isCancelled': None,
            'cancelReason': None,
            'delayReason': 'Delayed due to engineering work.',
            'adhocAlerts': None
        }
        service_status = get_service_status(service_item)
        service_status_expected =\
            ServiceStatus(Status.Delayed,
                          'Delay reason: Delayed due to engineering work.')

        self.assertEqual(service_status, service_status_expected)

    def test_return_adhoc_alerts_service_status(self):
        service_item = {
            'etd': 'On time',
            'isCancelled': None,
            'cancelReason': None,
            'delayReason': None,
            'adhocAlerts': ['Toilets are unavailable.',
                            'Doors are not working at first carriage.']
        }
        service_status = get_service_status(service_item)
        service_status_expected =\
            ServiceStatus(Status.OnTime,
                          ('Alerts:\nToilets are unavailable.'
                           '\nDoors are not working at first carriage.'))

        self.assertEqual(service_status, service_status_expected)


class TestGetServiceTime(unittest.TestCase):
    def test_return_scheduled_departure_time(self):
        service_item = {'std': '07:36',
                        'etd': 'On time'}
        service_time = get_service_time(service_item)
        service_time_expected = datetime.strptime('07:36', '%H:%M').time()

        self.assertEqual(service_time, service_time_expected)

    def test_return_estimated_departure_time(self):
        service_item = {'std': '07:36',
                        'etd': '07:37'}
        service_time = get_service_time(service_item)
        service_time_expected = datetime.strptime('07:37', '%H:%M').time()

        self.assertEqual(service_time, service_time_expected)


class TestGetCallingPointTime(unittest.TestCase):
    def test_return_time_from_at(self):
        calling_point = {'st': '00:41', 'et': '00:42', 'at': '00:42'}
        time_expected = '00:42'

        time = get_calling_point_time(calling_point)

        self.assertEqual(time, time_expected)

    def test_return_time_from_st(self):
        calling_point = {'st': '00:41', 'et': 'On time', 'at': None}
        time_expected = '00:41'

        time = get_calling_point_time(calling_point)

        self.assertEqual(time, time_expected)

    def test_return_time_from_et(self):
        calling_point = {'st': '00:41', 'et': '00:43', 'at': None}
        time_expected = '00:43'

        time = get_calling_point_time(calling_point)

        self.assertEqual(time, time_expected)


class TestIsCallingPointCancelled(unittest.TestCase):
    def test_return_cancelled(self):
        calling_point = {'isCancelled': True}

        cancelled = is_calling_point_cancelled(calling_point)

        self.assertTrue(cancelled)

    def test_return_not_cancelled(self):
        calling_point = {'isCancelled': None}

        cancelled = is_calling_point_cancelled(calling_point)

        self.assertFalse(cancelled)


class TestGetCallingPointAlert(unittest.TestCase):
    def test_return_no_adhoc_alerts_messages(self):
        calling_point = {'adhocAlerts': None}
        alert_message = get_calling_point_alert(calling_point)
        self.assertEqual(alert_message, '')

    def test_return_adhoc_alerts_message(self):
        alert_content = [
            'Lift at the station is not available.',
            'Toilet at the station is open.'
        ]
        calling_point = {'adhocAlerts': alert_content}
        alert_message = get_calling_point_alert(calling_point)
        self.assertEqual(alert_message, '\n'.join(alert_content))


class TestGetCallingPoint(unittest.TestCase):
    def test_return_calling_point(self):
        calling_point_data = {
            'locationName': 'Woolwich Arsenal',
            'st': '00:44',
            'et': 'On time',
            'at': None,
            'isCancelled': None,
            'adhocAlerts': None
        }
        calling_point = get_calling_point(calling_point_data)
        calling_point_expected =\
            CallingPoint('Woolwich Arsenal', '00:44', False, '')
        self.assertEqual(calling_point, calling_point_expected)


class TestGetCallingPoints(unittest.TestCase):
    def test_return_calling_points(self):
        service_item = {'subsequentCallingPoints': {
            'callingPointList': [{
                'callingPoint': [
                    {
                        'locationName': 'London Bridge',
                        'st': '14:26',
                        'et': 'On time',
                        'at': None,
                        'isCancelled': None,
                        'adhocAlerts': None
                    },
                    {
                        'locationName': 'London Waterloo East',
                        'st': '14:31',
                        'et': 'On time',
                        'at': None,
                        'isCancelled': None,
                        'adhocAlerts': None
                    },
                    {
                        'locationName': 'London Charing Cross',
                        'st': '14:35',
                        'et': 'On time',
                        'at': None,
                        'isCancelled': None,
                        'adhocAlerts': None
                    }]
                }]
            }
        }
        calling_point_names_included = {'London Bridge',
                                        'London Charing Cross'}
        calling_points_expected = [
            CallingPoint('London Bridge', '14:26', False, ''),
            CallingPoint('London Charing Cross', '14:35', False, '')
        ]
        calling_points = get_calling_points(service_item,
                                            calling_point_names_included)
        self.assertListEqual(calling_points, calling_points_expected)


class TestGetService(unittest.TestCase):
    def test_return_service(self):
        service_item = {
            'std': '13:06',
            'etd': '13:08',
            'platform': '1',
            'isCancelled': None,
            'length': 10,
            'cancelReason': None,
            'delayReason': None,
            'serviceID': 'Ejj51DopLBG4oePJ8QS1vw==',
            'adhocAlerts': None,
            'subsequentCallingPoints': {
                'callingPointList': [
                    {
                        'callingPoint': [
                            {
                                'locationName': 'Blackheath',
                                'crs': 'BKH',
                                'st': '13:11',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Lewisham',
                                'crs': 'LEW',
                                'st': '13:14',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Bridge',
                                'crs': 'LBG',
                                'st': '13:26',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Waterloo East',
                                'crs': 'WAE',
                                'st': '13:31',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Charing Cross',
                                'crs': 'CHX',
                                'st': '13:35',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            }
                        ],
                        'serviceType': 'train',
                        'serviceChangeRequired': 'false',
                        'assocIsCancelled': 'false'
                    }
                ]
            }
        }
        calling_point_names_included = {
            'London Charing Cross', 'London Cannon Street', 'London Victoria'
        }
        service_status_expected = ServiceStatus(Status.NewTime, '')
        service_expected = Service(
            'Ejj51DopLBG4oePJ8QS1vw==', service_status_expected,
            datetime.strptime('13:08', '%H:%M').time(),
            [CallingPoint('London Charing Cross', '13:35', False, '')])
        service_expected.set_length(10)
        service_expected.set_platform('1')
        service = get_service(service_item, calling_point_names_included)
        self.assertEqual(service, service_expected)


class TestIsValidService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calling_point_names_included =\
            ['London Charing Cross', 'London Cannon Street', 'London Victoria']

    def test_return_true(self):
        service_item = {'subsequentCallingPoints': {
            'callingPointList': [{
                'callingPoint': [
                    {'locationName': 'London Bridge'},
                    {'locationName': 'London Waterloo East'},
                    {'locationName': 'London Charing Cross'}]}]}
            }
        service_valid = is_valid_service(
            service_item, self.calling_point_names_included)
        self.assertTrue(service_valid)

    def test_return_false(self):
        service_item = {'subsequentCallingPoints': {
            'callingPointList': [{
                'callingPoint': [
                    {'locationName': 'Woolwich Dockyard'},
                    {'locationName': 'Woolwich Arsenal'},
                    {'locationName': 'Plumstead'}]}]}
            }
        service_valid = is_valid_service(
            service_item, self.calling_point_names_included)
        self.assertFalse(service_valid)


class TestGetServices(unittest.TestCase):
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

    @classmethod
    def setUpClass(cls):
        cls.service_1 = {
            'std': '13:06',
            'etd': '13:08',
            'platform': '1',
            'isCancelled': None,
            'length': 10,
            'cancelReason': None,
            'delayReason': None,
            'serviceID': 'Ejj51DopLBG4oePJ8QS1vw==',
            'adhocAlerts': None,
            'subsequentCallingPoints': {
                'callingPointList': [
                    {
                        'callingPoint': [
                            {
                                'locationName': 'Blackheath',
                                'crs': 'BKH',
                                'st': '13:11',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Lewisham',
                                'crs': 'LEW',
                                'st': '13:14',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Bridge',
                                'crs': 'LBG',
                                'st': '13:26',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Waterloo East',
                                'crs': 'WAE',
                                'st': '13:31',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Charing Cross',
                                'crs': 'CHX',
                                'st': '13:35',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'adhocAlerts': None
                            }
                        ],
                        'serviceType': 'train',
                        'serviceChangeRequired': 'false',
                        'assocIsCancelled': 'false'
                    }
                ]
            }
        }
        cls.service_2 = {
            'std': '13:10',
            'etd': 'On time',
            'platform': '1',
            'isCancelled': None,
            'length': 8,
            'cancelReason': None,
            'delayReason': None,
            'serviceID': 'puYuKPlAQWM7I2/xb5C3pQ==',
            'adhocAlerts': None,
            'subsequentCallingPoints': {
                'callingPointList': [
                    {
                        'callingPoint': [
                            {
                                'locationName': 'Westcombe Park',
                                'st': '13:12',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Maze Hill',
                                'st': '13:14',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Greenwich',
                                'st': '13:17',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Deptford',
                                'st': '13:19',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Bridge',
                                'st': '13:27',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Blackfriars',
                                'st': '13:34',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'City Thameslink',
                                'st': '13:36',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Farringdon',
                                'st': '13:38',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London St Pancras (Intl)',
                                'st': '13:43',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'West Hampstead Thameslink',
                                'st': '13:51',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Mill Hill Broadway',
                                'st': '14:00',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Elstree & Borehamwood',
                                'st': '14:05',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Radlett',
                                'st': '14:09',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'St Albans',
                                'st': '14:15',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            }
                        ],
                        'serviceType': 'train',
                        'serviceChangeRequired': 'false',
                        'assocIsCancelled': 'false'
                    }
                ]
            }
        }
        cls.service_3 = {
            'std': '13:20',
            'etd': 'On time',
            'platform': '1',
            'isCancelled': None,
            'length': 8,
            'cancelReason': None,
            'delayReason': None,
            'serviceID': '14etaXoW2Uyf34f3euTuUg==',
            'adhocAlerts': None,
            'subsequentCallingPoints': {
                'callingPointList': [
                    {
                        'callingPoint': [
                            {
                                'locationName': 'Westcombe Park',
                                'st': '13:22',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Maze Hill',
                                'st': '13:24',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Greenwich',
                                'st': '13:27',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'Deptford',
                                'st': '13:29',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Bridge',
                                'st': '13:35',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            },
                            {
                                'locationName': 'London Cannon Street',
                                'st': '13:41',
                                'et': 'On time',
                                'at': None,
                                'isCancelled': None,
                                'length': 8,
                                'adhocAlerts': None
                            }
                        ],
                        'serviceType': 'train',
                        'serviceChangeRequired': 'false',
                        'assocIsCancelled': 'false'
                    }
                ]
            }
        }

    def test_return_services(self):
        departure_board = {
            'trainServices': {
                'service': [self.service_1, self.service_2, self.service_3]
            }
        }
        calling_point_names_included = {'London Charing Cross',
                                        'London Cannon Street'}
        services_expected = [self.service_expected_1, self.service_expected_2]
        services = get_services(departure_board, calling_point_names_included)
        self.assertListEqual(services, services_expected)
