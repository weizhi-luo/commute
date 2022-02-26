"""Represent aws config settings"""
import json
from typing import Iterable, Mapping

import boto3
from datetime import datetime, timedelta

from data_model import OriginAndCallingPointNames
from .config import ConfigSettings


class AwsAppConfigSettings(ConfigSettings):
    """Represent a collection of config settings on AWS"""
    def __init__(self):
        """Create an instance of `AwsAppConfigSettings`"""
        self._origins_and_calling_points_config_session =\
            AwsAppConfigSession('stations_and_services_scraper', 'PROD',
                                'origins_and_calling_points', 1800)
        self._stations_crs_codes_config_session =\
            AwsAppConfigSession('stations_and_services_scraper', 'PROD',
                                'station_name_crs_code_mapping', 1800)
        self._darwin_config_session =\
            AwsAppConfigSession('stations_and_services_scraper', 'PROD',
                                'darwin', 1800)
        self._darwin_token =\
            json.loads(
                get_secret('darwin/token', 'eu-west-2')['SecretString']
            )['darwin_token']

    def get_services_origin_and_calling_point_names(self)\
            -> Iterable[OriginAndCallingPointNames]:
        """Get a collection of services' origin and calling point names

        :return: A collection of instances of `OriginAndCallingPointNames`
        """
        setting = json.loads(
            self._origins_and_calling_points_config_session.get_config())
        return [OriginAndCallingPointNames(**s) for s in setting]

    def get_data_access_config(self) -> Mapping:
        """Get config for setting up data access

        :return: Data access configuration
        """
        return {
            'station_name_crs_code_mapping':
                self._stations_crs_codes_config_session.get_config(),
            'wsdl':
                json.loads(self._darwin_config_session.get_config())['wsdl'],
            'token': self._darwin_token
        }

    def get_data_publisher_config(self) -> Mapping:
        """Get config for setting up data publish

        :return: Data publish configuration
        """
        return {}


class AwsAppConfigSession:
    """Represent an AWS app config session"""
    def __init__(self, application_identifier: str, environment: str,
                 profile_identifier: str, poll_interval_seconds: int):
        """Create an instance of `AwsAppConfigSession`

        :param application_identifier: Identifier of application
                                       related to the config
        :param environment: Environment of the config
        :param profile_identifier: Identifier of the config
        :param poll_interval_seconds: interval in seconds to pull config
        """
        self._application_identifier = application_identifier
        self._environment = environment
        self._profile_identifier = profile_identifier
        self._poll_interval_seconds = poll_interval_seconds
        self._config = None
        self._config_token = None

    def get_config(self) -> str:
        """Get and return config"""
        if self._config is None or self._config_token is None:
            self._start_session_and_get_latest_config()
        elif self._is_poll_interval_passed():
            self._get_latest_config()
        return self._config

    def _start_session_and_get_latest_config(self):
        self._start_session()
        self._get_latest_config()

    def _start_session(self):
        self._client = boto3.client('appconfigdata')
        response = self._client.start_configuration_session(
            ApplicationIdentifier=self._application_identifier,
            EnvironmentIdentifier=self._environment,
            ConfigurationProfileIdentifier=self._profile_identifier,
            RequiredMinimumPollIntervalInSeconds=self._poll_interval_seconds
        )
        self._config_token = response['InitialConfigurationToken']

    def _get_latest_config(self):
        response = self._client.get_latest_configuration(
            ConfigurationToken=self._config_token)
        self._config_token = response['NextPollConfigurationToken']
        self._poll_interval_seconds =\
            int(response['NextPollIntervalInSeconds'])
        self._last_get_latest_config_time = datetime.utcnow()
        self._update_config(response)

    def _update_config(self, response):
        config_bytes = response['Configuration'].read()
        if config_bytes != b'':
            self._config = config_bytes.decode('utf-8')

    def _is_poll_interval_passed(self):
        config_expiry_time = self._last_get_latest_config_time\
                             + timedelta(seconds=self._poll_interval_seconds)
        return config_expiry_time < datetime.utcnow()


def get_secret(secret_name: str, region_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager',
                            region_name=region_name)
    return client.get_secret_value(SecretId=secret_name)
