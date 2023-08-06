import sys

from ..base_request import BaseRequest
from ..settings import Settings


def _normalize_device_type(dev_type):
    if dev_type['state'] == 'PREVIEW':
        dev_type['state'] = 'ALPHA'
        dev_type['name'] = dev_type['name'].replace('(PREVIEW)', '(ALPHA)')
    if dev_type['state'] == 'EXPERIMENTAL':
        dev_type['state'] = 'BETA'
        dev_type['name'] = dev_type['name'].replace('(EXPERIMENTAL)', ('BETA'))
    if dev_type['slug'] == 'raspberry-pi':
        dev_type['name'] = 'Raspberry Pi (v1 or Zero)'
    return dev_type


class Config(object):
    """
    This class implements configuration model for Resin Python SDK.

    Attributes:
        _config (dict): caching configuration.

    """

    def __init__(self):
        self.base_request = BaseRequest()
        self.settings = Settings()
        self._config = None

    def _get_config(self, key):
        if self._config:
            return self._config[key]
        # Load all config again
        self.get_all()
        return self._config[key]

    def get_all(self):
        """
        Get all configuration.

        Returns:
            dict: configuration information.

        Examples:
            >>> resin.models.config.get_all()
            { all configuration details }

        """

        if self._config is None:
            self._config = self.base_request.request(
                'config', 'GET', endpoint=self.settings.get('api_endpoint'))
            self._config['deviceTypes'] = list(map(_normalize_device_type, self._config['deviceTypes']))
        return self._config

    def get_device_types(self):
        """
        Get device types configuration.

        Returns:
            list: device types information.

        Examples:
            >>> resin.models.config.get_device_types()
            [ all configuration details ]

        """

        return self._get_config('deviceTypes')
