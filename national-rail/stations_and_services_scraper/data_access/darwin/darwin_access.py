"""Represent access to Darwin web service"""
import json
import zeep
from typing import Mapping

from .station import get_station
from .service import get_services
from data_access import DataAccess
from error import StationCrsCodeNotFoundError
from data_model import OriginAndCallingPointNames, StationAndServices


class DarwinClient:
    """Represent the client to use Darwin soap web service"""

    def __init__(self, config: Mapping):
        """Create an instance of `DarwinDataAccess`

        :param config: Config settings for initialization
        """
        self._station_name_crs_code_mapping = \
            json.loads(config.get('station_name_crs_code_mapping'))
        self._client = self._create_soap_client(
            config.get('wsdl'))
        self._header = self._create_soap_headers(
            config.get('token'))

    @staticmethod
    def _create_soap_client(wsdl: str):
        return zeep.Client(wsdl=wsdl)

    @staticmethod
    def _create_soap_headers(token: str):
        header = zeep.xsd.Element(
            '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
            zeep.xsd.ComplexType([zeep.xsd.Element(
                ('{http://thalesgroup.com/RTTI/2013-11-28/Token/types}'
                 'TokenValue'), zeep.xsd.String())]))
        return header(TokenValue=token)

    def get_departure_board_with_details(self, station_name: str) -> Mapping:
        """Get departure board with details from Darwin web service

        :param station_name: Name of the station
        :return: Departure board with details from Darwin web service
        """
        station_crs_code = self._get_station_crs_code(station_name)
        return self._client.service.GetDepBoardWithDetails(
            numRows=100, crs=station_crs_code, _soapheaders=[self._header])

    def _get_station_crs_code(self, station_name: str) -> str:
        station_crs_code = \
            self._station_name_crs_code_mapping.get(station_name, None)
        if not station_crs_code:
            raise StationCrsCodeNotFoundError(
                f'Station crs code cannot be found for {station_name}')
        return station_crs_code


class DarwinDataAccess(DataAccess):
    """Represent access to national rail data provided by Darwin"""

    def __init__(self, config: Mapping):
        """Create an instance of `DarwinDataAccess`

        :param config: Config settings for initialization
        """
        self._client = DarwinClient(config)

    def get_station_and_services(
            self, origin_and_calling_point_names: OriginAndCallingPointNames)\
            -> StationAndServices:
        """Get station and related services

        :param origin_and_calling_point_names: The service's origin and
                                               calling point names
        :return: an instance of `StationAndServices`
        """
        origin_name = origin_and_calling_point_names.origin_name
        calling_point_names_included =\
            origin_and_calling_point_names.calling_point_names
        departure_board =\
            self._client.get_departure_board_with_details(origin_name)
        return get_station_and_services(departure_board,
                                        calling_point_names_included)


def get_station_and_services(
        departure_board_with_details, calling_point_names_included)\
        -> StationAndServices:
    station = get_station(departure_board_with_details)
    services = get_services(departure_board_with_details,
                            calling_point_names_included)
    return StationAndServices(station, services)
