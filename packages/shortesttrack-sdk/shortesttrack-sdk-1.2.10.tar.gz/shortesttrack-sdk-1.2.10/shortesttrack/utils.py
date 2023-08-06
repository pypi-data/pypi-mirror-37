import os

import requests
from shortesttrack_tools.api_client import BaseApiClient, SecAccessTokenMixin
from shortesttrack_tools.logger.utils import get_prototype_logger
from shortesttrack.conf.lib_conf import ULibraryConfig


# Backward compatibility
getLogger = get_prototype_logger


def do_post(url, headers, body: dict = None) -> requests.Response:
    body = body if body else {}

    response = requests.post(url=url, headers=headers, json=body)

    if response.status_code not in (200, 201):
        raise Exception(response.status_code)

    return response


def do_get(url, headers) -> requests.Response:
    response = requests.get(url, headers=headers)

    if response.status_code not in (200, 201):
        raise Exception(response.status_code)

    return response


class APIClient(BaseApiClient, SecAccessTokenMixin):
    # TODO: these variables are deprecated, it is for backward compatibility
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
        _token = ULibraryConfig.sec_refresh_token
        if not _token:
            # TODO: backward compatibility. Remove this behavior in v1.3
            _token = self.SEC_REFRESH_TOKEN
        return _token

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
        return get_prototype_logger('api-client')

    def _set_cache_sec_access_token_expiration(self, configuration_id, expiration):
        self.TOKEN_EXPIRATIONS[configuration_id] = expiration
