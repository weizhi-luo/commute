"""Represent config data"""
import json
import boto3
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class ConfigData(ABC):
    """Represent config data"""
    @abstractmethod
    def get(self) -> str:
        """Get raw config data

        :return: Raw config data in string
        """
        pass


class ConfigDataAwsS3(ConfigData):
    """Represent config data stored by AWS S3 service"""
    def __init__(self, bucket_name: str, key_name: str):
        """Create an instance of `ConfigDataAwsS3`

        :param bucket_name: Bucket name the S3 session connected to
        :param key_name: Key name the S3 session connected to
       """
        self._s3 = boto3.resource('s3')
        self._bucket_name = bucket_name
        self._key_name = key_name
        self._config_data = None

    def get(self) -> str:
        """Get raw config data from a key in AWS S3 bucket

        :return: Raw config data in string
        """
        if self._config_data is None:
            s3_object = self._s3.Object(
                bucket_name=self._bucket_name, key=self._key_name)
            self._config_data = s3_object.get()['Body'].read()
        return self._config_data


class ConfigDataAwsSecretManager(ConfigData):
    """Represent config data stored by AWS secret manager service"""
    def __init__(self, region_name: str, secret_name: str, secret_key) -> None:
        """Create an instance of `ConfigDataAwsSecretManager`

        :param region_name: region of secret manager service
        :param secret_name: secret name
        :param secret_key: secret key that the value mapped to
        :return: an instance of `ConfigDataAwsSecretManager`
        """
        self._region_name = region_name
        self._secret_name = secret_name
        self._secret_key = secret_key
        self._config_data = None

    def get(self) -> str:
        """Get raw config data from AWS secret manager service

        :return: Raw config data in string
        """
        if self._config_data is None:
            session = boto3.session.Session()
            client = session.client(service_name='secretsmanager',
                                    region_name=self._region_name)
            self._config_data = json.loads(
                client.get_secret_value(SecretId=self._secret_name)
                ['SecretString'])[self._secret_key]
        return self._config_data


class ConfigDataAwsAppConfig(ConfigData):
    """Represent config data stored AWS AppConfig service"""
    def __init__(self, application_identifier: str, environment: str,
                 profile_identifier: str, poll_interval_seconds: int):
        """Create an instance of `ConfigDataAwsAppConfig`

        :param application_identifier: Identifier of application
                                       related to the config_access
        :param environment: Environment of the config_access
        :param profile_identifier: Identifier of the config_access
        :param poll_interval_seconds: interval in seconds to pull config_access
        """
        self._application_identifier = application_identifier
        self._environment = environment
        self._profile_identifier = profile_identifier
        self._poll_interval_seconds = poll_interval_seconds
        self._config = None
        self._config_token = None

    def get(self) -> str:
        """Get raw config data from a key in AWS AppConfig

        :return: Raw config data in string
        """
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
