import os
from typing import List
import requests
import logging

from notifications.common import Resource, NotificationClient
from notifications.utils import _random_string

from notifications.fields import BaseBlock, Attachment

ACCESS_TOKEN = None
ACCESS_TOKEN_ENV_NAME = 'SLACK_ACCESS_TOKEN'


logger = logging.getLogger(__name__)


class SlackError(requests.exceptions.RequestException):
    pass


class SlackMessage:
    def __init__(self, client, response,
                 text: str = None,
                 raise_exc=False,
                 attachments: List[Attachment] = None,
                 blocks: List[BaseBlock] = None):
        super().__init__(client, response, text, raise_exc, attachments, blocks)
        self._client = client
        self._response = response
        self._raise_exc = raise_exc

        self.text = text
        self.attachments = attachments or []
        self.blocks = blocks or []

        self.__lock_thread = False

    @property
    def response(self):
        return self._response

    def _lock_thread(self):
        self.__lock_thread = True

    def send_to_thread(self, **kwargs):
        if self.__lock_thread:
            raise SlackError('Cannot open thread for thread message')

        json = self._response.json()
        thread_ts = json['message']['ts']
        kwargs.update(thread_ts=thread_ts)

        message = self._client.send_notify(json['channel'], **kwargs)

        lock_thread = getattr(message, '_lock_thread')
        lock_thread()

        return message

    def update(self):
        json = self._response.json()
        data = {
            'channel': json['channel'],
            'ts': json['message']['ts'],
        }

        if self.text:
            data['text'] = self.text

        if self.blocks:
            data['blocks'] = [b.to_dict() for b in self.blocks]

        if self.attachments:
            data['attachments'] = [a.to_dict() for a in self.attachments]

        return self._client.call_resource(
            Resource('chat.update', 'POST'),
            json=data, raise_exc=self._raise_exc,
        )

    def delete(self):
        json = self._response.json()
        data = {
            'channel': json['channel'],
            'ts': json['message']['ts'],
        }
        return self._client.call_resource(
            Resource('chat.update', 'POST'),
            json=data, raise_exc=self._raise_exc,
        )

    def upload_file(self, file, **kwargs):
        json = self._response.json()
        kwargs.update(thread_ts=json['message']['ts'])
        return self._client.upload_file(json['channel'], file, **kwargs)

    def add_reaction(self, name, raise_exc=False):
        json = self._response.json()
        data = {
            'name': name,
            'channel': json['channel'],
            'timestamp': json['message']['ts'],
        }
        return self._client.call_resource(
            Resource('reactions.add', 'POST'),
            json=data, raise_exc=raise_exc,
        )

    def remove_reaction(self, name, raise_exc=False):
        json = self._response.json()
        data = {
            'name': name,
            'channel': json['channel'],
            'timestamp': json['message']['ts'],
        }
        return self._client.call_resource(
            Resource('reactions.remove', 'POST'),
            json=data, raise_exc=raise_exc,
        )


class Slack(NotificationClient):
    API_URL = 'https://slack.com/api'

    def __init__(self, token: str):
        super().__init__(self.API_URL, token=token)

    @classmethod
    def from_env(cls):
        token = ACCESS_TOKEN or os.getenv(ACCESS_TOKEN_ENV_NAME)
        assert token is not None, 'Please export "{}" environment variable'.format(ACCESS_TOKEN_ENV_NAME)
        return cls(token)

    def send_notification(self,
                          channel, *,
                          text: str = None,
                          username: str = None,
                          icon_url: str = None,
                          icon_emoji: str = None,
                          link_names: bool = True,
                          raise_exc: bool = False,
                          attachments: List = None,
                          blocks: List = None,
                          thread_ts: str = None) -> SlackMessage:
        data = {
            'channel': channel,
            'link_names': link_names,
        }

        if username:
            data['username'] = username

        if text:
            data['mrkdwn'] = True
            data['text'] = text

        if icon_url:
            data['icon_url'] = icon_url

        if icon_emoji:
            data['icon_emoji'] = icon_emoji

        if blocks:
            data['blocks'] = [b.to_dict() for b in blocks]

        if attachments:
            data['attachments'] = [a.to_dict() for a in attachments]

        if thread_ts:
            data['thread_ts'] = thread_ts

        response = self.call_resource(
            Resource('chat.postMessage', 'POST'), raise_exc=raise_exc, json=data,
        )
        return SlackMessage(self, response, text=text, raise_exc=raise_exc, blocks=blocks, attachments=attachments)

    def upload_file(self,
                    channel, file, *,
                    title: str = None,
                    content: str = None,
                    filename: str = None,
                    thread_ts: str = None,
                    filetype: str = 'text',
                    raise_exc: bool = False):
        data = {
            'channels': channel,
            'filetype': filetype,
        }
        if isinstance(file, str) and content:
            filename = file
            data.update(content=content, filename=filename)
        elif isinstance(file, str) and not content:
            data.update(filename=os.path.basename(file))
            with open(file, 'r') as f:
                data.update(content=f.read())
        else:
            data.update(content=file.read(), filename=filename or _random_string(7))

        if title:
            data.update(title=title)
        if thread_ts:
            data.update(thread_ts=thread_ts)

        return self.call_resource(
            Resource('files.upload', 'POST'),
            data=data,
            raise_exc=raise_exc,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        )


def call_resource(*args, **kwargs):
    return Slack.from_env().call_resource(*args, **kwargs)


def resource_iterator(*args, **kwargs):
    return Slack.from_env().resource_iterator(*args, **kwargs)


def send_notify(*args, **kwargs):
    return Slack.from_env().send_notification(*args, **kwargs)
