"""Run the application in AWS lambda"""
import json

from main import scrape_and_publish_stations_and_services


def lambda_handler(event, context):
    scrape_and_publish_stations_and_services()

    return {
        'statusCode': 200,
        'body': json.dumps('Finished scraping and publishing '
                           'stations and services')
    }
