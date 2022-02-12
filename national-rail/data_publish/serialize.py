"""Represent serializer for data"""
import datetime
import json
from json import JSONEncoder
from abc import ABC, abstractmethod


class StringDataSerializer(ABC):
    """Represent serializer that serialize data to string"""
    @abstractmethod
    def serialize(self, data: object) -> str:
        """Serialize data

        :param data: Data to be serialized
        :return: Serialized data in string format
        """
        pass


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.time):
            return o.strftime('%H:%M')
        return o.__dict__


class JsonDataSerializer(StringDataSerializer):
    """Represent a serializer for serializing data to json format"""
    def __init__(self, encoder=Encoder):
        self._encoder = encoder

    def serialize(self, data: object) -> str:
        """Serialize data

        :param data: Data to be serialized
        :return: Serialized data in string format
        """
        return json.dumps(data, cls=self._encoder, indent=4)
