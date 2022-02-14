"""Represent config settings"""
from abc import ABC, abstractmethod
from typing import Mapping, Iterable
import json

from data_model import OriginAndCallingPointNames


class ConfigSettings(ABC):
    @abstractmethod
    def get(self, name: str) -> str:
        """Get config setting based on the name provided

        :param name: Name of the setting
        :return: Value of the setting
        """
        pass


class AwsAppConfigSettings(ConfigSettings):
    def get(self, name: str) -> str:
        """Get config setting based on the name provided

        :param name: Name of the setting
        :return: Value of the setting
        """
        raise NotImplemented()


def get_data_access_config(config_settings: ConfigSettings) -> Mapping:
    """Get config for setting up data access

    :param config_settings: An instance of `ConfigSettings`
    :return: Data access configuration
    """
    return json.loads(config_settings.get('data_access'))


def get_services_origin_and_calling_point_names(
        config_settings: ConfigSettings)\
        -> Iterable[OriginAndCallingPointNames]:
    """Get a collection of services' origin and calling point names

    :param config_settings: An instance of `ConfigSettings`
    :return: A collection of instances of `OriginAndCallingPointNames`
    """
    setting = json.loads(
        config_settings.get('services_origin_and_calling_point_names'))
    return [OriginAndCallingPointNames(**s) for s in setting]


def get_data_publisher_config(config_settings: ConfigSettings) -> Mapping:
    """Get config for setting up data publish

    :param config_settings: An instance of `ConfigSettings`
    :return: Data publish configuration
    """
    return json.loads(config_settings.get('data_publish'))
