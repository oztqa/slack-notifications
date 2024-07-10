import os
from typing import List
import logging
import requests

from notifications.interfaces import Message, NotificationClient, Resource
from notifications.mettermost.fields import BaseBlock, Attachment

ACCESS_TOKEN = None
ACCESS_TOKEN_ENV_NAME = 'SLACK_ACCESS_TOKEN'
BASE_URL = None
BASE_URL_ENV_NAME = 'METTERMOST_URL'
TEAM_ID = None
TEAM_ID_ENV_NAME = 'SLACK_ACCESS_TOKEN'

logger = logging.getLogger(__name__)


class SlackError(requests.exceptions.RequestException):
    pass


class MettermostMessage(Message):
    def send_to_thread(self, **kwargs):
        json = self._response.json()
        message_id = json['id']
        kwargs.update(root_id=message_id)

        message = self._client.send_notification(json['channel_id'], **kwargs)

        return message

    def update(self):
        json = self._response.json()
        data = {
            'id': json['id'],
            'message': self.text or '',
            'props': {},
            'metadata': {}
        }
        if self.blocks:
            data['message'] += ''.join(map(str, self.blocks))

        if self.attachments:
            data['props']['attachments'] = [a.convert() for a in self.attachments]

        return self._client.call_resource(
            Resource('posts/{post_id}', 'PUT'),
            json=data, raise_exc=self._raise_exc,
        )

    def delete(self):
        message_id = self._response.json()['id']
        response = self._client.call_resource(
            Resource(f'posts/{message_id}', 'DELETE'),
            raise_exc=self._raise_exc
        )
        return response

    def upload_file(self, file, **kwargs):
        pass

    def add_reaction(self, name, raise_exc=False):
        json = self._response.json()
        data = {
            'emoji_name': name,
            'post_id': json['id'],
            'user_id': json['user_id'],
            'create_at': json['create_at']
        }
        return self._client.call_resource(
            Resource('reactions', 'POST'),
            json=data, raise_exc=raise_exc,
        )

    def remove_reaction(self, name, raise_exc=False):
        json = self._response.json()
        user_id = json['user_id']
        post_id = json['post_id']

        return self._client.call_resource(
            Resource(f'users/{user_id}/posts/{post_id}/reactions/{name}', 'DELETE'),
            raise_exc=raise_exc,
        )


class Mettermost(NotificationClient):

    def __init__(self, base_url, *, token, team_id, **kwargs):
        super(Mettermost, self).__init__(base_url, token=token, **kwargs)
        self._team_id = team_id

    def channel_id_by_name(self, channel_name):
        response = self.call_resource(Resource(f'teams/{self._team_id}/channels/name/{channel_name}', 'GET'))

        if response.status_code != 200:
            raise ValueError('Channel not found')

        return response.json()['id']

    @classmethod
    def from_env(cls):
        token = ACCESS_TOKEN or os.getenv(ACCESS_TOKEN_ENV_NAME)
        base_url = BASE_URL or os.getenv(BASE_URL_ENV_NAME)
        team_id = TEAM_ID or os.getenv(TEAM_ID_ENV_NAME)

        return cls(base_url, token=token, team_id=team_id)

    def send_notification(self,
                          channel: str, *,
                          text=None,
                          blocks: List[BaseBlock] = None,
                          attachments: List[Attachment] = None,
                          file_ids: List[str] = None,
                          root_id: str = None,
                          priority: str = None,
                          raise_exc: bool = False,
                          requested_ack: bool = False):

        data = {
            'channel_id': self.channel_id_by_name(channel),
            'message': text or '',
            'props': {},
            'metadata': {}
        }
        if blocks:
            data['message'] += ''.join(map(str, blocks))

        if root_id:
            data['root_id'] = root_id

        if attachments:
            data['props']['attachments'] = [a.convert() for a in attachments]

        if file_ids:
            data['file_ids'] = file_ids

        if priority or requested_ack:
            data['metadata']['priority'] = {'priority': priority or 'empty', 'requested_ack': requested_ack}

        response = self.call_resource(
            Resource('posts', 'POST'), json=data,
        )
        return MettermostMessage(
            self, response, text=text, raise_exc=raise_exc,  blocks=blocks, attachments=attachments
        )

    def upload_file(self, *args, **kwargs):
        pass
