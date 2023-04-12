"""Represent service data"""
from .calling_point import CallingPoint

from enum import Enum
from dataclasses import dataclass
from datetime import time
from typing import Iterable


class Status(str, Enum):
    OnTime = 'OnTime'
    NewTime = 'NewTime'
    Cancelled = 'Cancelled'
    Delayed = 'Delayed'


@dataclass
class ServiceStatus:
    """Represent status of a service

    Attributes:

    - :class:`Status` status: status of the service
    - :class:`str` abnormality_message: message when the service is abnormal
    """
    status: Status
    abnormality_message: str


@dataclass
class Service:
    """Represent a service

    Attributes:

    - :class:`str` id: service identifier
    - :class:`ServiceStatus` status: service status
    - :class:`time` time: service departure time
    - :class:`Iterable[CallingPoint]` calling_points: service's calling points
    - :class:`int` length: service length
    - :class:`str` platform: platform that the service uses
    """
    id: str
    status: ServiceStatus
    time: time
    calling_points: Iterable[CallingPoint]
    length: int = None
    platform: str = None
