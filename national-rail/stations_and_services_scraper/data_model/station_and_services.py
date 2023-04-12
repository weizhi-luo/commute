"""Represent station and services data"""
from .station import Station
from .service import Service

from typing import Iterable
from dataclasses import dataclass


@dataclass
class StationAndServices:
    """Represent a station and related services

    Attributes:

    - :class:`Station` station: railway station
    - :class:`Iterable[Service]` services: services at the railway station
    """
    station: Station
    services: Iterable[Service]
