"""Represent transformer for data scraped from Darwin API"""
from .transformer import StationAndServicesTransformer
from data_model import StationAndServices, Station, Service, ServiceStatus, \
    Status, CallingPoint

from typing import Mapping, Iterable
from datetime import datetime, time


class DarwinStationAndServicesTransformer(StationAndServicesTransformer):
    """Represent transform for station and services data from Darwin"""

    def transform(self, raw_data: Mapping) -> StationAndServices:
        """Transform raw data to station and services

        :param raw_data: raw data
        :return: an instance of `StationAndServices`
        """
        station = self._get_station(raw_data)
        services = self._get_services(raw_data)
        return StationAndServices(station, services)

    @staticmethod
    def _get_station(departure_board: Mapping) -> Station:
        name = departure_board['locationName']
        are_services_available = \
            departure_board['areServicesAvailable'] is not False
        message = '' if not departure_board['nrccMessages'] else '\n'.join(
            m['_value_1'] for m in departure_board['nrccMessages']['message'])
        return Station(name, are_services_available, message)

    def _get_services(self, departure_board: Mapping) -> Iterable[Service]:
        services = departure_board['trainServices']
        return [] if not services else [self._get_service(service) for
                                        service in services['service']]

    def _get_service(self, service: Mapping) -> Service:
        id_ = service['serviceID']
        status = self._get_service_status(service)
        time_ = self._get_service_time(service)
        calling_points = self._get_calling_points(service)
        length = service['length']
        platform = service['platform']
        return Service(id_, status, time_, calling_points, length, platform)

    def _get_service_status(self, service: Mapping) -> ServiceStatus:
        status = self._get_status(service)
        abnormality_message = self._get_abnormality_message(service)
        return ServiceStatus(status, abnormality_message)

    @staticmethod
    def _get_status(service: Mapping) -> Status:
        is_on_time = service['etd'].casefold().strip() == 'on time'
        is_cancelled = service['etd'].casefold().strip() == 'cancelled' \
            or service['isCancelled']
        is_delayed = service['etd'].casefold().strip() == 'delayed'
        return Status.Cancelled if is_cancelled \
            else Status.Delayed if is_delayed \
            else Status.OnTime if is_on_time else Status.NewTime

    @staticmethod
    def _get_abnormality_message(service: Mapping) -> str:
        messages = []
        if service['cancelReason']:
            messages.append(f'Cancel reason: {service["cancelReason"]}')
        if service['delayReason']:
            messages.append(f'Delay reason: {service["delayReason"]}')
        if service['adhocAlerts']:
            alerts = '\n'.join(service["adhocAlerts"])
            messages.append(f'Alerts:\n{alerts}')
        return '\n'.join(messages)

    @staticmethod
    def _get_service_time(service: Mapping) -> time:
        scheduled_departure_time = service['std']
        estimated_departure_time = service['etd']
        return datetime.strptime(scheduled_departure_time, '%H:%M').time() \
            if estimated_departure_time.casefold().strip() == 'on time' \
            else datetime.strptime(estimated_departure_time, '%H:%M').time()

    def _get_calling_points(self, service: Mapping) -> Iterable[CallingPoint]:
        calling_points = service['subsequentCallingPoints'][
            'callingPointList'][0]['callingPoint']
        return list(map(self._get_calling_point, calling_points))

    def _get_calling_point(self, calling_point: Mapping) -> CallingPoint:
        name = calling_point['locationName']
        time_ = self._get_calling_point_time(calling_point)
        is_cancelled = calling_point['isCancelled']
        alert = '' if not calling_point['adhocAlerts'] \
            else '\n'.join(calling_point['adhocAlerts'])
        return CallingPoint(name, time_, is_cancelled, alert)

    @staticmethod
    def _get_calling_point_time(calling_point: Mapping) -> str:
        if calling_point['at']:
            return calling_point['at']
        if calling_point['et'].casefold().strip() == 'on time':
            return calling_point['st']
        return calling_point['et']
