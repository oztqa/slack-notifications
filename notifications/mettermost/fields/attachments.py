from typing import List

from notifications.constants import COLOR_MAP
from notifications.interfaces.fields import ConvertibleObject


class AttachmentField(ConvertibleObject):

    def __init__(self, *, title: str = None, value: str = None, short: bool = False):
        super(AttachmentField, self).__init__()

        self.title = title
        self.value = value
        self.short = short

    def convert(self):
        assert self.title is not None or self.value is not None, \
            'Title or value is required for attachment field'

        data = {'short': self.short}

        if self.title:
            data['title'] = self.title

        if self.value:
            data['value'] = self.value

        return data


class ActionField:
    __type__ = None

    def __init__(self, name: str, action_id: str, integration_payload: dict = None, style: str = None,  **kwargs):
        super(ActionField, self).__init__(**kwargs)
        self.action_id = action_id
        self.name = name
        self.integration = integration_payload
        self.style = style

    def convert(self):
        data = {
            'id': self.action_id,
            'type': self.__type__,
            'name': self.name,
            'integration': self.integration,
        }

        if self.style is not None:
            data['style'] = self.style

        return data


class ButtonField(ActionField):
    __type__ = 'button'


class OptionField:
    def __init__(self, text: str, value: str):
        super(OptionField, self).__init__()
        self.text = text
        self.value = value

    def convert(self):
        data = {'text': self.text, 'value': self.value}
        return data


class MenuField(ActionField):
    __type__ = 'select'

    def __init__(self, *, options: List[OptionField] = None, data_source: str = None, **kwargs):
        if not data_source and not options:
            raise ValueError('Options or data is required for menu fields')

        super(MenuField, self).__init__(**kwargs)
        self.options = options
        self.data_source = data_source

    def convert(self):
        data = super(MenuField, self).convert()

        data['options'] = self.options

        if self.data_source is not None:
            data['data_source'] = self.data_source

        return data


class Attachment(ConvertibleObject):
    Field = AttachmentField

    def __init__(self, *,
                 image_url: str = None,
                 thumb_url: str = None,
                 author_name: str = None,
                 author_icon: str = None,
                 author_link: str = None,
                 title: str = None,
                 title_link: str = None,
                 fallback: str = None,
                 color: str = None,
                 pretext: str = None,
                 text: str = None,
                 footer: str = None,
                 footer_icon: str = None,
                 fields: List[AttachmentField] = None,
                 actions: List[ActionField] = None
                 ):
        super(Attachment, self).__init__()
        self.fallback = fallback

        self.image_url = image_url
        self.thumb_url = thumb_url

        self.author_name = author_name
        self.author_link = author_link
        self.author_icon = author_icon

        self.title = title
        self.title_link = title_link

        self.pretext = pretext
        self.text = text

        self.footer = footer
        self.footer_icon = footer_icon

        self.fields = fields
        self.actions = actions

        self.color = color

    def convert(self):
        data = {}

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

        if self.title_link:
            data['title_link'] = self.title_link

        if self.pretext:
            data['pretext'] = self.pretext

        if self.text:
            data['text'] = self.text

        if self.footer:
            data['footer'] = self.footer

        if self.footer_icon:
            data['footer_icon'] = self.footer_icon

        if self.fields:
            data['fields'] = [f.convert() for f in self.fields]

        if self.actions:
            data['actions'] = [f.convert() for f in self.actions]

        return data
