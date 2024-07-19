import requests
import logging

logger = logging.getLogger(__name__)


class DictConvertibleObject:

    def __init__(self, *args, **kwargs):
        pass

    def to_dict(self):
        raise NotImplementedError(
            'Object "{}" does not implemented "to_dict" method'.format(self.__class__.__name__),
        )


class NotificationError(requests.exceptions.RequestException):
    pass


class Resource:
    def __init__(self, handle: str, method: str):
        self.handle = handle
        self.method = method


class NotificationClient(requests.Session):
    DEFAULT_RECORDS_LIMIT = 100
    DEFAULT_REQUEST_TIMEOUT = 180

    def __init__(self, base_url, *, token):
        self.base_url = base_url
        self._token = token
        super().__init__()

        self.headers['Authorization'] = 'Bearer {}'.format(token)
        self.headers['Content-Type'] = 'application/json; charset=utf-8'

    def call_resource(self, resource: Resource, *, raise_exc: bool = False, **kwargs):
        kwargs.setdefault('timeout', self.DEFAULT_REQUEST_TIMEOUT)

        url = '{}/{}'.format(self.base_url, resource.handle)
        response = self.request(resource.method, url, **kwargs)

        logger.debug(response.content)

        if raise_exc:
            response.raise_for_status()

            if not response.ok:
                logger.error(response.content)
                raise NotificationError(response.content)

        return response
