import requests
from requests.auth import HTTPBasicAuth
from urlobject import URLObject

from shortesttrack.utils import getLogger
from shortesttrack.client.access_token import AccessToken

logger = getLogger(__name__)


class AuthHelper:
    def __init__(self, host: str) -> None:
        logger.info(f'AuthHelper {host}')
        self._host = host

    def get_access_token_from_username(self, username: str, password: str, company_id: str) -> AccessToken:
        data = [
            ('grant_type', 'password'), ('username', username),
            ('password', password), ('company_id', company_id)
        ]
        url = URLObject(self._host).add_path('/api/uaa/authenticate')
        logger.info(f'get_access_token_from_username: {url} {data}')
        response = requests.Request('POST', url, data=data).prepare()

        return AccessToken(response)

    def get_access_token_from_refresh_token(self, refresh_token: str) -> AccessToken:
        data = 'grant_type=refresh_token&client_id=script&refresh_token={}'.format(refresh_token)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        url = URLObject(self._host).add_path('/oauth/token')

        logger.info(f'get_access_token_from_refresh_token: {url} {headers} {data}')
        response = requests.Request(
            'POST', url, data=data, headers=headers, auth=HTTPBasicAuth('script', 'noMatter', )
        ).prepare()

        return AccessToken(response)
