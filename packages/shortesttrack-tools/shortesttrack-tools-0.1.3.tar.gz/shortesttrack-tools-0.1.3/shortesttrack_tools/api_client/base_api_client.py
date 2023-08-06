import abc

import requests
import six
from requests import Response
from requests.auth import HTTPBasicAuth
from urlobject import URLObject
from collections import OrderedDict


@six.add_metaclass(abc.ABCMeta)
class BaseApiClient(object):
    def __init__(self, host=None, *args, **kwargs):
        from shortesttrack_tools.api_client.endpoints.endpoint_urls import EndpointURLs
        self.logger = self._get_logger()
        self.endpoint_urls = EndpointURLs.init(host=host)
        self.host = self.endpoint_urls.HOST
        self.GET = 'GET'
        self.POST = 'POST'
        self.PATCH = 'PATCH'
        self.DELETE = 'DELETE'

    @abc.abstractmethod
    def _get_logger(self):
        """
        Return a logger object

        """

    @abc.abstractmethod
    def _raise_http_error(self, exception: requests.HTTPError, message):
        """
        Raise appropriate exception when HTTP error is occurred

        """

    @abc.abstractmethod
    def _raise_performing_request_error(self, message):
        """
        Raise appropriate exception when Request cannot be performed

        """

    @abc.abstractmethod
    def _get_auth_string(self):
        """
        Return auth user string
        """

    def _construct_response_message(self, response: Response) -> str:
        message = f'Response:'
        message += f' [{response.status_code}]'

        if response.reason:
            message += f' [{response.reason}]'

        if response.content:
            try:
                decoded_content = response.content.decode()
            except Exception as e:
                decoded_content = f' (ERROR: content cannot be decoded: error {e})'
            else:
                decoded_content = ' ' + decoded_content

            decoded_content = decoded_content[:2048]
            message += decoded_content
        else:
            message += ' (ERROR: no content in response)'

        return message

    def _construct_http_error_message(self, response: Response) -> str:
        message = 'HTTPError: '
        message += self._construct_response_message(response)
        return message

    def prepare_auth(self, basic_auth_tuple: tuple, sec_id_for_special_token: str) -> tuple:
        assert not (basic_auth_tuple and sec_id_for_special_token), 'Only one of these args can be specified'
        if basic_auth_tuple:
            # The basic auth can be used instead of normal Bearer auth
            return HTTPBasicAuth(*basic_auth_tuple), {}, False

        # Normal Bearer auth
        if sec_id_for_special_token:
            assert hasattr(self, 'get_sec_access_token'), 'Method does not exist. Forgot Mixin?'
            # This param is overriding auth with SEC token auth
            return None, 'Bearer {}'.format(self.get_sec_access_token(sec_id_for_special_token)), True

        # Use user auth
        return None, self._get_auth_string(), False

    def request(
            self,
            http_method,
            path,
            base: str,
            params=None,
            data=None,
            json=None,
            basic_auth_tuple=None,
            sec_id_for_special_token=None,
            extra_headers=None,
            raw_content=False,
            files=None
    ):
        auth, auth_header, retry = self.prepare_auth(basic_auth_tuple, sec_id_for_special_token)

        if path.startswith('/'):
            path = path[1:]

        url = URLObject(base).add_path(path)

        headers = {}
        if not files:
            headers['Content-Type'] = 'application/json'

        if auth_header:
            headers['Authorization'] = auth_header

        if extra_headers:
            headers.update(extra_headers)

        def _request():
            try:
                _log_post_data = None

                if json:
                    _log_post_data = json
                elif data:
                    _log_post_data = '(Binary Data)'

                if _log_post_data:
                    _log_post_data = str(_log_post_data)[:2048]

                calling_service_message = f'Calling service {http_method} : {url} : {headers}'
                if _log_post_data:
                    calling_service_message += f' : {_log_post_data}'

                self.logger.info(calling_service_message)
                resp_ = requests.request(http_method, url,
                                         params=params, data=data, json=json, headers=headers, files=files, auth=auth)
            except requests.RequestException as e_:
                self.logger.error('Outer service request error: {}'.format(e_))
                self._raise_performing_request_error('Error on request performing: {}'.format(e_))

            self.logger.info(self._construct_response_message(resp_))
            return resp_

        resp = _request()
        try:
            resp.raise_for_status()
        except requests.HTTPError as e1:
            if retry and resp.status_code in [401, 403]:
                self._retry_occurred()
                # Probably sec_access_token is expired, let's get a new one
                _, auth_header, _ = self.prepare_auth(basic_auth_tuple, sec_id_for_special_token)
                if auth_header:
                    headers['Authorization'] = auth_header

                # Retry request
                resp = _request()
                try:
                    resp.raise_for_status()
                except requests.HTTPError as e2:
                    # This is not access_token expiration, raise exception
                    http_error_message = self._construct_http_error_message(resp)
                    self._raise_http_error(e2, http_error_message)
            else:
                http_error_message = self._construct_http_error_message(resp)
                self._raise_http_error(e1, http_error_message)

        except Exception as e:
            # This error should never be happened
            self.logger.error('Unexpected error (it can be error in base_api_client module): {}'.format(e))
            raise

        if not raw_content:
            return resp.json(object_pairs_hook=OrderedDict)

        return resp.content

    def _retry_occurred(self):
        """
        This method is overridden for test purposes. By default it's do nothing and don't need to be overridden.
        """
