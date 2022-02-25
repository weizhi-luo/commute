"""Functions for publishing data"""
from typing import Iterable, Mapping
from abc import ABC, abstractmethod

from data_model import StationAndServices
from .serialize import StringDataSerializer


class DataPublisher(ABC):
    """Represent data publisher"""
    @abstractmethod
    def publish(self, data: object) -> None:
        """Publish data

        :param data: Data be published
        :return: None
        """
        pass


class AwsDataPublisher(DataPublisher):
    """Represent data publisher to AWS"""

    def __init__(self, config: Mapping, serializer: StringDataSerializer):
        """Create an instance of `AWSDataPublisher`

        :param config: Config settings for initialization
        :param serializer: Serializer that serializes data to string
        """
        self._serializer = serializer

    def publish(self, data: object) -> None:
        """Publish station and services

        :param data: Station and services to be published
        :return: None
        """
        serialized_data = self._serializer.serialize(data)
        print(serialized_data)


def publish(data_publisher: DataPublisher,
            stations_and_services: Iterable[StationAndServices]) -> None:
    """Publish a collection of station and services

    :param data_publisher: Data publisher
    :param stations_and_services: A collection of `StationAndServices`
    :return: None
    """
    data_publisher.publish(stations_and_services)
