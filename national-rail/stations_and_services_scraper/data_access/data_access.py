"""Represent access to national rail data"""
from abc import ABC, abstractmethod

from data_model import OriginAndCallingPointNames, StationAndServices


class DataAccess(ABC):
    """Represent access to national rail data"""
    @abstractmethod
    def get_station_and_services(
            self, origin_and_calling_point_names: OriginAndCallingPointNames)\
            -> StationAndServices:
        """Get station and related services

        :param origin_and_calling_point_names: The service's origin and
                                               calling point names
        :return: an instance of `StationAndServices`
        """
        pass
