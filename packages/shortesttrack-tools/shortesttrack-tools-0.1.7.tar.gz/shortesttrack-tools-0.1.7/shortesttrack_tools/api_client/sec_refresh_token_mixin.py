import abc

import six


@six.add_metaclass(abc.ABCMeta)
class SecRefreshTokenMixin(object):
    @abc.abstractmethod
    def _get_cache_sec_refresh_token(self, configuration_id):
        """
        Return sec refresh token from cache

        """

    @abc.abstractmethod
    def _set_cache_sec_refresh_token(self, configuration_id, refresh_token):
        """
        Set sec refresh token to cache

        """

    def get_sec_refresh_token(self, configuration_id):
        refresh_token = self._get_cache_sec_refresh_token(configuration_id)

        if not refresh_token:
            json = self.request(self.GET, 'api-keys/{}'.format(configuration_id),
                                base=self.endpoint_urls.UAA_SERVICE_ENDPOINT)
            refresh_token = json['refreshTokenValue']
            self._set_cache_sec_refresh_token(configuration_id, refresh_token)

        return refresh_token
