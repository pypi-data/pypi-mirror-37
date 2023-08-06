import json

import requests

from shortesttrack.utils import getLogger, do_post

import warnings


warnings.warn('This module is deprecated.', DeprecationWarning, stacklevel=2)


logger = getLogger()


# TODO: use APIClient for requests


class ISSConnector:
    def __init__(self, url: str, auth_custom_token: str = None) -> None:
        self._url = url
        logger.info(f'ISSConnector {url} {auth_custom_token}')
        self._auth_custom_token = auth_custom_token

    def send(self, msg: dict) -> bytes:
        headers = {'Auth-Custom-Token': self._auth_custom_token} if self._auth_custom_token else {}
        return do_post(self._url, headers, msg).content

    def is_health(self) -> bool:
        try:
            r = requests.get(self._url.replace('iter', 'healthz'))
            return json.loads(r.content.decode())['message'] == 'OK'
        except:
            logger.exception(f'Service {self._url} is not healthy')
            return False

    def is_ready(self) -> bool:
        try:
            r = requests.get(self._url.replace('iter', 'readyz'))
            return json.loads(r.content.decode())['message'] == 'OK'
        except:
            logger.exception(f'Service {self._url} is not ready')
            return False
