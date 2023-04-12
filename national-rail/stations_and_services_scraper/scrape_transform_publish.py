"""Represent functions to scraper, transformer and publish data"""
from scrape import StationAndServicesScraper
from transform import StationAndServicesTransformer
from publish import StationAndServicesPublisher

from typing import Iterable


def scrape_transform_publish_station_and_services(
        scraper: StationAndServicesScraper,
        transformer: StationAndServicesTransformer,
        publisher: StationAndServicesPublisher, station: str,
        calling_points: Iterable[str]) -> None:
    """Scrape, transformer and publish station and services data

    :param scraper: station and services data scraper
    :param transformer: station and services data transformer
    :param publisher: station and services data publisher
    :param station: station where data is scraped
    :param calling_points: target calling points served by the services
    :return: None
    """
    raw_data = scraper.scrape(station, calling_points)
    station_and_services = transformer.transform(raw_data)
    publisher.publish(station_and_services)
