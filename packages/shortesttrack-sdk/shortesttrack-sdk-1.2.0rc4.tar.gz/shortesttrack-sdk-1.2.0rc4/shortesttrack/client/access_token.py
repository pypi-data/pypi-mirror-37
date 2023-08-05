import requests
from requests import PreparedRequest
from time import time

from shortesttrack.utils import getLogger

logger = getLogger()


class AccessToken:
    def __init__(self, request: PreparedRequest, update_interval: int = 30) -> None:
        self._request = request
        self._last_update = 0
        self._update_interval = update_interval
        self._token = self.get()

    def get(self) -> str:
        if time() - self._last_update < self._update_interval:
            logger.info(f'access token {self._token}')
            return self._token

        s = requests.Session()
        response = s.send(self._request)
        if response.status_code not in (200, 201):
            logger.error(response.content)
            raise Exception(response.status_code)

        self._token = response.json()['access_token']
        self._last_update = time()

        logger.info(f'update access token {self._token}')
        return self._token
