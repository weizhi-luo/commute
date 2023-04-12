"""Represent calling point data"""
from dataclasses import dataclass


@dataclass
class CallingPoint:
    """Represent a service's calling point

    Attributes:

    - :class:`str` name: name of the calling point
    - :class:`str` time: time that the train service arrives
    - :class:`bool` is_cancelled: indicate if calling point is cancelled
    - :class:`str` alert: alert at this calling point
    """
    name: str
    time: str
    is_cancelled: bool
    alert: str
