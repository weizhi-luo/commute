"""Represent Darwin data scraper"""
from .scraper import StationAndServicesScraper

import zeep
from typing import Mapping, Iterable


class DarwinStationAndServicesScraper(StationAndServicesScraper):
    """Represent station and services scraper from Darwin data API"""

    def __init__(self, token: str, station_name_crs_code_mapping: Mapping):
        """Create an instance of `DarwinStationAndServicesScraper`

        :param token: Token to access Darwin API
        :param station_name_crs_code_mapping: Mapping between station name
        and National Rail CRS code
        """
        self._soap_client = zeep.Client(
            wsdl=('http://lite.realtime.nationalrail.co.uk/'
                  'OpenLDBWS/wsdl.aspx?ver=2017-10-01'))
        self._soap_header = self._create_soap_headers(token)
        self._station_name_crs_code_mapping = station_name_crs_code_mapping

    @staticmethod
    def _create_soap_headers(token: str):
        header = zeep.xsd.Element(
            '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
            zeep.xsd.ComplexType([zeep.xsd.Element(
                ('{http://thalesgroup.com/RTTI/2013-11-28/Token/types}'
                 'TokenValue'), zeep.xsd.String())]))
        return header(TokenValue=token)

    def scrape(self, origin: str, destination: str) -> Mapping:
        """Scrape station and services

        :param origin: origin station name
        :param destination: destination station name
        :return: origin station and services related to destination
        """
        station_crs_code = self._get_station_crs_code(origin)
        departure_board = self._soap_client.service.GetDepBoardWithDetails(
            numRows=20, crs=station_crs_code, timeOffset=0, timeWindow=120,
            _soapheaders=[self._soap_header])
        raise NotImplementedError()

    def _get_station_crs_code(self, station_name: str) -> str:
        station_crs_code = \
            self._station_name_crs_code_mapping.get(station_name, None)
        if not station_crs_code:
            raise KeyError(
                f'Station crs code cannot be found for {station_name}')
        return station_crs_code

    @staticmethod
    def _filter_departure_board(departure_board: Mapping, destination: str) \
            -> Mapping:
        train_services = []
        for service in departure_board['trainServices']['service']:
            if any(filter(lambda l: l['locationName'] == destination,
                          service['destination']['location'])):
                train_services.append(service)
            else:

        departure_board['trainServices']['service'] = train_services
        return departure_board
