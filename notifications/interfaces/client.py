from typing import List
import requests
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class NotificationError(requests.exceptions.RequestException):
    pass


class Resource:
    def __init__(self, handle: str, method: str):
        self.handle = handle
        self.method = method


class Message(ABC):
    def __init__(self, client, response,
                 text: str = None,
                 raise_exc=False,
                 attachments: List = None,
                 blocks: List = None):
        self._client = client
        self._response = response
        self._raise_exc = raise_exc

        self.text = text
        self.attachments = attachments or []
        self.blocks = blocks or []

    @property
    def response(self):
        return self._response

    @abstractmethod
    def send_to_thread(self, **kwargs):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def upload_file(self, file, **kwargs):
        pass

    @abstractmethod
    def add_reaction(self, name, raise_exc=False):
        pass

    @abstractmethod
    def remove_reaction(self, name, raise_exc=False):
        pass


class NotificationClient(requests.Session, ABC):
    DEFAULT_RECORDS_LIMIT = 100
    DEFAULT_REQUEST_TIMEOUT = 180

    def __init__(self, base_url, *, token, **kwargs):
        self.base_url = base_url
        self._token = token
        super().__init__(**kwargs)

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

    def resource_iterator(self,
                          resource: Resource, from_key: str, *,
                          cursor: str = None,
                          raise_exc: bool = False,
                          limit: int = None):
        params = {'limit': limit}

        if cursor:
            params['cursor'] = cursor

        response = self.call_resource(resource, params=params, raise_exc=raise_exc)
        data = response.json()

        for item in data[from_key]:
            yield item

        cursor = data.get('response_metadata', {}).get('next_cursor')

        if cursor:
            yield from self.resource_iterator(
                resource, from_key,
                limit=limit or self.DEFAULT_RECORDS_LIMIT, cursor=cursor, raise_exc=raise_exc,
            )

    @classmethod
    @abstractmethod
    def from_env(cls):
        pass

    @abstractmethod
    def send_notification(
            self, channel: str, *,
            text: str = None, attachments: List = None, blocks: List = None,
            **kwargs) -> Message:
        pass

    @abstractmethod
    def upload_file(self, *args, **kwargs):
        pass
