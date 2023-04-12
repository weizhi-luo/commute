"""Represent station data"""
from dataclasses import dataclass


@dataclass
class Station:
    """Represent a station

    Attributes:

    - :class:`str` name: name of the station
    - :class:`bool` are_services_available: indicate if services are available
    - :class:`str` message: message at the station
    """
    name: str
    are_services_available: bool
    message: str
