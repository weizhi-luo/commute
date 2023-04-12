"""Represent data publishers"""
from data_model import StationAndServices

from abc import ABC, abstractmethod
from typing import Iterable


class StationAndServicesPublisher(ABC):
    """Represent station and services data publisher"""

    @abstractmethod
    def publish(self, station_and_services: StationAndServices) -> None:
        """Publish station and services data

        :param station_and_services: an instance of `StationAndServices`
        :return: None
        """
        pass
