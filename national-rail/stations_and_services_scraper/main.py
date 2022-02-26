"""Run the application"""
from config import AwsAppConfigSettings
from data_access import DarwinDataAccess
from data_scrape import scrape_stations_and_services
from data_publish import ConsoleDataPublisher, JsonDataSerializer, publish


def scrape_and_publish_stations_and_services():
    config_setting = AwsAppConfigSettings()
    data_access_config = config_setting.get_data_access_config()
    # data_publisher_config = config_setting.get_data_publisher_config()
    services_origin_and_calling_point_names = \
        config_setting.get_services_origin_and_calling_point_names()

    data_access = DarwinDataAccess(data_access_config)
    data_publisher = ConsoleDataPublisher(JsonDataSerializer())

    stations_and_services = scrape_stations_and_services(
        data_access, services_origin_and_calling_point_names)
    publish(data_publisher, stations_and_services)


if __name__ == '__main__':
    scrape_and_publish_stations_and_services()
