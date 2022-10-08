"""Run the application"""
from config_access import ConfigAccessFromConfigDataSet
from config_data import ConfigDataAwsS3, ConfigDataAwsSecretManager
from data_access import DarwinDataAccess
from data_scrape import scrape_stations_and_services
from data_publish import ConsoleDataPublisher, JsonDataSerializer, publish


def scrape_and_publish_stations_and_services():
    config_access = \
        ConfigAccessFromConfigDataSet(*create_config_data_collection())
    data_access_config = config_access.get_data_access_config()
    # data_publisher_config = config_settings.get_data_publisher_config()
    services_origin_and_calling_point_names = \
        config_access.get_services_origin_and_calling_point_names()

    data_access = DarwinDataAccess(data_access_config)
    data_publisher = ConsoleDataPublisher(JsonDataSerializer())

    stations_and_services = scrape_stations_and_services(
        data_access, services_origin_and_calling_point_names)
    publish(data_publisher, stations_and_services)


def create_config_data_collection():
    origins_and_calling_points_config_data = ConfigDataAwsS3(
        'stations-and-services-scraper', 'origins_and_calling_points.json')
    stations_crs_codes_config_data = ConfigDataAwsS3(
        'stations-and-services-scraper', 'station_name_crs_code_mapping.json')
    darwin_access_config_data = \
        ConfigDataAwsS3('stations-and-services-scraper', 'darwin.json')
    darwin_token_config_data = \
        ConfigDataAwsSecretManager('eu-west-2', 'darwin/token', 'darwin_token')
    return origins_and_calling_points_config_data, \
        stations_crs_codes_config_data, darwin_access_config_data, \
        darwin_token_config_data


if __name__ == '__main__':
    scrape_and_publish_stations_and_services()
