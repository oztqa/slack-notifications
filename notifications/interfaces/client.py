from typing import Protocol, List

from notifications.fields.blocks import BaseBlock
from notifications.fields.attachments import Attachment


class InterfaceMessage(Protocol):

    def send_to_thread(self, **kwargs):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def upload_file(self, file, **kwargs):
        pass

    def add_reaction(self, name, raise_exc=False):
        pass

    def remove_reaction(self, name, raise_exc=False):
        pass


class InterfaceClient(Protocol):
    def send_notify(self,
                    channel, *,
                    text: str = None,
                    username: str = None,
                    icon_url: str = None,
                    icon_emoji: str = None,
                    link_names: bool = True,
                    raise_exc: bool = False,
                    attachments: List[Attachment] = None,
                    blocks: List[BaseBlock] = None,
                    thread_ts: str = None) -> InterfaceMessage:
        pass

    def upload_file(self,
                    channel, file, *,
                    title: str = None,
                    content: str = None,
                    filename: str = None,
                    thread_ts: str = None,
                    filetype: str = 'text',
                    raise_exc: bool = False):
        pass
