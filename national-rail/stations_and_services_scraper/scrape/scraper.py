"""Represent data scraper"""
from abc import ABC, abstractmethod
from typing import Iterable


class StationAndServicesScraper(ABC):
    """Represent station and services scraper"""

    @abstractmethod
    def scrape(self, origin: str, destination: str) -> object:
        """Scrape station and services

        :param origin: origin station name
        :param destination: destination station name
        :return: origin station and services related to destination
        """
        pass
