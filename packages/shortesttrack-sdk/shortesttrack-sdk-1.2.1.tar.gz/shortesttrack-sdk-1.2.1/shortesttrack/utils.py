import os
import sys
import logging

import requests
from shortesttrack_tools.api_client import BaseApiClient, SecAccessTokenMixin

APPLICATION_LOG_NAME = 'shortesttrack-sdk'
DEFAULT_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

LOG_LEVEL = 'INFO'
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(DEFAULT_FORMATTER)
root_logger.addHandler(stream_handler)


def getLogger(short_name: str = None, log_level: str = LOG_LEVEL):
    name = _get_qualified_name(short_name)
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger


def _get_qualified_name(name: str) -> str:
    if name:
        return f'{APPLICATION_LOG_NAME}.{name}'

    return APPLICATION_LOG_NAME


def do_post(url, headers, body: dict = None) -> requests.Response:
    body = body if body else {}
    root_logger.info(f'request POST: {url} {body}')
    root_logger.debug(f'request POST: {url} {headers} {body}')

    response = requests.post(url=url, headers=headers, json=body)
    root_logger.info(f'response: {response.status_code} {response.content}')

    if response.status_code not in (200, 201):
        raise Exception(response.status_code)

    return response


def do_get(url, headers) -> requests.Response:
    root_logger.info(f'request GET: {url}')
    root_logger.debug(f'request GET: {url} {headers}')

    response = requests.get(url, headers=headers)
    root_logger.info(f'response: {response.status_code} {response.content}')

    if response.status_code not in (200, 201):
        raise Exception(response.status_code)

    return response


class APIClient(BaseApiClient, SecAccessTokenMixin):
    SEC_REFRESH_TOKEN = os.environ.get('SEC_REFRESH_TOKEN')
    ISSC_ID = os.environ.get('ISSC_ID')
    CONFIGURATION_ID = os.environ.get('CONFIGURATION_ID')
    ASEC_ID = os.environ.get('ASEC_ID')
    PERFORMANCE_ID = os.environ.get('PERFORMANCE_ID')

    # Token data
    PUBLIC_KEY = None
    TOKENS = {}
    TOKEN_EXPIRATIONS = {}

    @property
    def _basic_auth_tuple(self) -> tuple:
        return 'script', 'noMatter'

    def _raise_http_error(self, exception: requests.HTTPError, message):
        raise Exception(message)

    def _get_cache_sec_access_token_expiration(self, configuration_id):
        return self.TOKEN_EXPIRATIONS.get(configuration_id)

    def _get_auth_string(self):
        return ''

    def get_sec_refresh_token(self, configuration_id):
        return self.SEC_REFRESH_TOKEN

    def _get_cache_public_key(self):
        return self.PUBLIC_KEY

    def _set_cache_public_key(self, public_key):
        self.PUBLIC_KEY = public_key

    def _set_cache_sec_access_token(self, configuration_id, access_token):
        self.TOKENS[configuration_id] = access_token

    def _get_cache_sec_access_token(self, configuration_id):
        return self.TOKENS.get(configuration_id)

    def _raise_performing_request_error(self, *args, **kwargs):
        raise Exception(*args, **kwargs)

    def _get_logger(self):
        return root_logger

    def _set_cache_sec_access_token_expiration(self, configuration_id, expiration):
        self.TOKEN_EXPIRATIONS[configuration_id] = expiration
