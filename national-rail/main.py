"""Run the application"""
from config import get_data_access_config, get_data_publisher_config,\
                   get_services_origin_and_calling_point_names,\
                   AwsAppConfigSettings
from data_access import DarwinDataAccess
from data_scrape import scrape_stations_and_services
from data_publish import AwsDataPublisher, JsonDataSerializer, publish


def scrape_and_publish_stations_and_services():
    config_setting = AwsAppConfigSettings()

    data_access = DarwinDataAccess(get_data_access_config(config_setting))
    services_origin_and_calling_point_names =\
        get_services_origin_and_calling_point_names(config_setting)
    data_publisher = AwsDataPublisher(
        get_data_publisher_config(config_setting), JsonDataSerializer())

    stations_and_services = scrape_stations_and_services(
        data_access, services_origin_and_calling_point_names)
    publish(data_publisher, stations_and_services)


if __name__ == '__main__':
    scrape_and_publish_stations_and_services()
