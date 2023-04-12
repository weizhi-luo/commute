"""Represent route data"""
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
class Route:
    """Represent a route

    Attributes:

    - :class:`str` service_id: the route's train service identifier
    - :class:`str` origin: the route's origin
    - :class:`time` departing_time: departing time from origin
    - :class:`str` destination: the route's destination
    - :class:`time` arriving_time: arriving time at destination
    - :class:`Iterable[CallingPoint]` calling_points: route's calling points
    - :class:`Status` status: the route's status
    - :class:`str` message: the route's message
    - :class:`int` length: the route's train service length
    - :class:`str` platform: platform that the route's train service uses
    """
    service_id: str
    origin: str
    departing_time: time
    destination: str
    arriving_time: time
    calling_points: Iterable[CallingPoint]
    status: Status
    message: str
    length: int = None
    platform: str = None
