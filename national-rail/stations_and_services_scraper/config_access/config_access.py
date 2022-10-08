"""Represent config_access settings"""
from abc import ABC, abstractmethod
from typing import Mapping, Iterable
import json

from data_model import OriginAndCallingPointNames
from config_data import ConfigData


class ConfigAccess(ABC):
    """Represent access to configuration"""

    @abstractmethod
    def get_data_access_config(self) -> Mapping:
        """Get data access config

        :return: Data access configuration
        """
        pass

    @abstractmethod
    def get_services_origin_and_calling_point_names(self)\
            -> Iterable[OriginAndCallingPointNames]:
        """Get a collection of services' origin and calling point names

        :return: A collection of instances of `OriginAndCallingPointNames`
        """
        pass

    @abstractmethod
    def get_data_publisher_config(self) -> Mapping:
        """Get data publisher config

        :return: Data publisher configuration
        """
        pass


class ConfigAccessFromConfigDataSet(ConfigAccess):
    """Represent a collection of config data"""
    def __init__(self, origins_and_calling_points_config_data: ConfigData,
                 stations_crs_codes_config_data: ConfigData,
                 darwin_access_config_data: ConfigData,
                 darwin_token_config_data: ConfigData) -> None:
        """Create an instance of `ConfigAccessFromConfigDataSet`

        :param origins_and_calling_points_config_data: origins and calling
                                                       points config data
        :param stations_crs_codes_config_data: stations crs codes config data
        :param darwin_access_config_data: darwin access config data
        :param darwin_token_config_data: darwin token config data
        :return: An instance of `ConfigAccessFromConfigDataSet`
        """
        self._origins_and_calling_points_config_data = \
            origins_and_calling_points_config_data.get()
        self._stations_crs_codes_config_data = \
            stations_crs_codes_config_data.get()
        self._darwin_access_config_data = darwin_access_config_data.get()
        self._darwin_token_config_data = darwin_token_config_data.get()

    def get_data_access_config(self) -> Mapping:
        """Get data access config

        :return: Data access configuration
        """
        return {
            'station_name_crs_code_mapping':
                self._stations_crs_codes_config_data,
            'wsdl': json.loads(self._darwin_access_config_data)['wsdl'],
            'token': self._darwin_token_config_data
        }

    def get_services_origin_and_calling_point_names(self) \
            -> Iterable[OriginAndCallingPointNames]:
        """Get a collection of services' origin and calling point names

        :return: A collection of instances of `OriginAndCallingPointNames`
        """
        setting = json.loads(self._origins_and_calling_points_config_data)
        return [OriginAndCallingPointNames(**s) for s in setting]

    def get_data_publisher_config(self) -> Mapping:
        """Get data publisher config

        :return: Data publish configuration
        """
        return {}
