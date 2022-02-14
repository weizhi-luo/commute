"""Represent data models"""
import datetime
from enum import Enum
from typing import Iterable, Set


class OriginAndCallingPointNames:
    """Represent a service's origin and calling point names"""
    def __init__(self, origin_name: str, calling_point_names: Set[str]):
        """Create an instance of `OriginAndCallingPointNames`

        :param origin_name: Name of origin of this service
        :param calling_point_names: Names of calling points of this service
        """
        self.origin_name = origin_name
        self.calling_point_names = calling_point_names


class Station:
    """Represent a station"""
    def __init__(self, name: str, are_services_available: bool, message: str):
        """Create an instance of `Station`

        :param name: Name of the station
        :param are_services_available: Indicate if the services are available
                                       at the station
        :param message: Message at the station
        """
        self.name = name
        self.are_services_available = are_services_available
        self.message = message

    def __eq__(self, other):
        return isinstance(other, Station)\
               and self.name == other.name\
               and self.are_services_available == other.are_services_available\
               and self.message == other.message


class Status(str, Enum):
    OnTime = 'OnTime'
    NewTime = 'NewTime'
    Cancelled = 'Cancelled'


class ServiceStatus:
    """Represent status of a service"""
    def __init__(self, status: Status, abnormality_message: str):
        """Create an instance of `ServiceStatus`

        :param status: Status of the service
        :param abnormality_message: Message when the service is abnormal
        """
        self.status = status
        self.abnormality_message = abnormality_message

    def __eq__(self, other):
        return isinstance(other, ServiceStatus)\
               and self.status == other.status\
               and self.abnormality_message == other.abnormality_message


class CallingPoint:
    """Represent a service's calling point"""
    def __init__(self, name: str, time: str, is_cancelled: bool, alert: str):
        """Create an instance of `CallingPoint`

        :param name: Calling point name
        :param time: Time that the service arrives
        :param is_cancelled: Indicate if this calling point is cancelled
        :param alert: Alert at this calling point
        """
        self.name = name
        self.time = time
        self.is_cancelled = is_cancelled
        self.alert = alert

    def __eq__(self, other):
        return isinstance(other, CallingPoint)\
            and self.name == other.name\
            and self.time == other.time\
            and self.is_cancelled == other.is_cancelled\
            and self.alert == other.alert


class Service:
    """Represent a service"""
    def __init__(self, id_: str, status: ServiceStatus, time: datetime.time,
                 calling_points: Iterable[CallingPoint]):
        """Create an instance of `Service`

        :param id_: Service identifier
        :param status: Service status
        :param time: Time that the service departs
        :param calling_points: Service's calling points
        """
        self.id = id_
        self.status = status
        self.time = time
        self.calling_points = calling_points
        self.length = None
        self.platform = None

    def set_length(self, length: int) -> None:
        """Set service length

        :param length: Service length
        :return: None
        """
        self.length = length

    def set_platform(self, platform: str) -> None:
        """Set service platform

        :param platform: Service platform
        :return: None
        """
        self.platform = platform

    def __eq__(self, other):
        return isinstance(other, Service)\
            and self.id == other.id\
            and self.status == other.status\
            and self.time == other.time\
            and self.calling_points == other.calling_points\
            and self.length == other.length\
            and self.platform == other.platform


class StationAndServices:
    """Represent a station and related service"""
    def __init__(self, station: Station, services: Iterable[Service]):
        """Create an instance of `StationAndServices`

        :param station: Railway station
        :param services: Services of interest at the station
        """
        self.station = station
        self.services = services

    def __eq__(self, other):
        return isinstance(other, StationAndServices)\
            and self.station == other.station\
            and self.services == other.services
