"""Run the application in AWS lambda"""
import json

from scrape_transform_publish import \
    scrape_transform_publish_station_and_services
from main import scrape_and_publish_stations_and_services


def lambda_handler(event, _):
    origin_name = event['origin_name']
    calling_point_names = event['calling_points']

    scrape_transform_publish_station_and_services()

    scrape_and_publish_stations_and_services()

    return {
        'statusCode': 200,
        'body': json.dumps('Finished scraping and publishing '
                           'stations and services.')
    }
