"""Represent data transformers"""
from data_model import StationAndServices

from abc import ABC, abstractmethod


class StationAndServicesTransformer(ABC):
    """Represent station and services data transformer"""

    @abstractmethod
    def transform(self, raw_data: object) -> StationAndServices:
        """Transform raw data to station and services

        :param raw_data: raw data
        :return: an instance of `StationAndServices`
        """
        pass
