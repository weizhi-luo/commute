"""Functions for scraping data"""
from typing import Iterable

from data_access import DataAccess
from data_model import OriginAndCallingPointNames, StationAndServices


def scrape_stations_and_services(data_access: DataAccess,
                                 services_origin_and_calling_point_names:
                                 Iterable[OriginAndCallingPointNames])\
        -> Iterable[StationAndServices]:
    """Scrape stations and services data from national rail

    :param data_access: Access to national rail data
    :param services_origin_and_calling_point_names: Services' origin and 
                                                    calling point names
    :return: A collection of `StationAndServices`
    """
    return list(map(data_access.get_station_and_services,
                    services_origin_and_calling_point_names))
