import logging
import sys

from shortesttrack_tools.api_client import BaseApiClient, SecAccessTokenMixin


APPLICATION_LOG_NAME = 'image-builder'
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


class APIClient(BaseApiClient, SecAccessTokenMixin):
    def __init__(self, host, sec_id, issc_id, sec_refresh_token):
        self._host = host
        self._sec_id = sec_id
        self._issc_id = issc_id
        self._sec_refresh_token = sec_refresh_token
        self._token_expiration = None
        self._token = None
        self._public_key = None
        super().__init__(host=host)

    @property
    def _basic_auth_tuple(self):
        return ('script', 'noMatter',)

    def _raise_http_error(self, exception, message):
        raise Exception(message)

    def _get_cache_sec_access_token_expiration(self, configuration_id):
        return self._token_expiration

    def _get_auth_string(self):
        return ''

    def get_sec_refresh_token(self, configuration_id):
        return self._sec_refresh_token

    def _get_cache_public_key(self):
        return self._public_key

    def _set_cache_public_key(self, public_key):
        self._public_key = public_key

    def _set_cache_sec_access_token(self, configuration_id, access_token):
        self._token = access_token

    def _get_cache_sec_access_token(self, configuration_id):
        return self._token

    def _raise_performing_request_error(self, *args, **kwargs):
        raise Exception(*args, **kwargs)

    def _get_logger(self):
        return getLogger('APIClient')

    def _set_cache_sec_access_token_expiration(self, configuration_id, expiration):
        self._token_expiration = expiration
