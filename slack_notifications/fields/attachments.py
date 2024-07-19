from typing import List

from slack_notifications.common import DictConvertibleObject
from slack_notifications.constants import COLOR_MAP


class AttachmentField(DictConvertibleObject):

    def __init__(self, *, title: str = None, value: str = None, short: bool = False):
        super(AttachmentField, self).__init__()

        self.title = title
        self.value = value
        self.short = short

    def to_dict(self):
        assert self.title is not None or self.value is not None, \
            'Title or value is required for attachment field'

        data = {'short': self.short}

        if self.title:
            data['title'] = self.title

        if self.value:
            data['value'] = self.value

        return data


class Attachment(DictConvertibleObject):
    Field = AttachmentField

    def __init__(self, *,
                 image_url: str = None,
                 thumb_url: str = None,
                 author_name: str = None,
                 author_link: str = None,
                 author_icon: str = None,
                 title: str = None,
                 title_link: str = None,
                 text: str = None,
                 pretext: str = None,
                 footer: str = None,
                 footer_icon: str = None,
                 timestamp: str = None,
                 fields: List[AttachmentField] = None,
                 mrkdwn: bool = True,
                 color: str = None):
        super(Attachment, self).__init__()

        self.image_url = image_url
        self.thumb_url = thumb_url

        self.author_name = author_name
        self.author_link = author_link
        self.author_icon = author_icon

        self.title = title
        self.title_link = title_link

        self.text = text

        self.pretext = pretext

        self.footer = footer
        self.footer_icon = footer_icon

        self.timestamp = timestamp

        self.fields = fields

        self.mrkdwn = mrkdwn
        self.color = color

    def to_dict(self):
        data = {
            'mrkdwn_in': [],
        }

        if self.color:
            data['color'] = COLOR_MAP.get(self.color, self.color)

        if self.image_url:
            data['image_url'] = self.image_url

        if self.thumb_url:
            data['thumb_url'] = self.thumb_url

        if self.author_name:
            data['author_name'] = self.author_name

        if self.author_link:
            data['author_link'] = self.author_link

        if self.author_icon:
            data['author_icon'] = self.author_icon

        if self.title:
            data['title'] = self.title
            if self.mrkdwn:
                data['mrkdwn_in'].append('title')

        if self.title_link:
            data['title_link'] = self.title_link

        if self.pretext:
            data['pretext'] = self.pretext
            if self.mrkdwn:
                data['mrkdwn_in'].append('pretext')

        if self.text:
            data['text'] = self.text
            if self.mrkdwn:
                data['mrkdwn_in'].append('text')

        if self.footer:
            data['footer'] = self.footer
            if self.mrkdwn:
                data['mrkdwn_in'].append('footer')

        if self.footer_icon:
            data['footer_icon'] = self.footer_icon

        if self.timestamp:
            data['ts'] = self.timestamp

        if self.fields:
            data['fields'] = [f.to_dict() for f in self.fields]
            if self.mrkdwn:
                data['mrkdwn_in'].append('fields')

        return data
