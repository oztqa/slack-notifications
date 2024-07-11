from typing import List, Union

from notifications.common import DictConvertibleObject


class BaseBlock(DictConvertibleObject):
    __type__ = None

    def __init__(self, *, mrkdwn: bool = True, block_id: str = None):
        super(BaseBlock, self).__init__()

        self.mrkdwn = mrkdwn
        self.block_id = block_id
        self.content_type = 'mrkdwn' if self.mrkdwn else 'plain_text'

    def to_dict(self):
        data = {
            'type': self.__type__,
        }

        if self.block_id:
            data['block_id'] = self.block_id

        return data

    def accept(self, converter):
        raise NotImplementedError(
            'Object "{}" does not implemented "accept" method'.format(self.__class__.__name__),
        )


class BaseBlockField(DictConvertibleObject):
    __type__ = None

    def __init__(self, *, mrkdwn=True):
        super(BaseBlockField, self).__init__()

        self.mrkdwn = mrkdwn
        self.content_type = 'mrkdwn' if self.mrkdwn else 'plain_text'

    def to_dict(self):
        if self.__type__:
            return {
                'type': self.__type__,
            }

        return {}


class HeaderBlock(BaseBlock):
    __type__ = 'header'

    def __init__(self, text: str, **kwargs):
        kwargs['mrkdwn'] = False
        super().__init__(**kwargs)

        self.text = text

    def to_dict(self):
        data = super().to_dict()

        data['text'] = {
            'type': self.content_type,
            'text': self.text,
        }

        return data

    def accept(self, converter):
        return converter.convert_header_block(self)


class SimpleTextBlockField(BaseBlockField):

    def __init__(self, text: str, *, emoji: bool = None, **kwargs):
        super(SimpleTextBlockField, self).__init__(**kwargs)

        self.text = text
        self.emoji = emoji

    def to_dict(self):
        data = super(SimpleTextBlockField, self).to_dict()

        data['text'] = self.text
        data['type'] = self.content_type

        if self.emoji is not None:
            data['emoji'] = self.emoji

        return data

    def accept(self, converter):
        return converter.convert_simple_text_block_field(self)


class SimpleTextBlock(BaseBlock):
    __type__ = 'section'

    Field = SimpleTextBlockField

    def __init__(self, text: str, *, fields: List[SimpleTextBlockField] = None, **kwargs):
        super(SimpleTextBlock, self).__init__(**kwargs)

        self.text = text
        self.fields = fields

    def to_dict(self):
        data = super(SimpleTextBlock, self).to_dict()

        data['text'] = {
            'type': self.content_type,
            'text': self.text,
        }

        if self.fields:
            data['fields'] = [f.to_dict() for f in self.fields]

        return data

    def accept(self, converter):
        return converter.convert_simple_text_block(self)


class DividerBlock(BaseBlock):
    __type__ = 'divider'

    def accept(self, converter):
        return converter.convert_divider_block(self)


class ImageBlock(BaseBlock):
    __type__ = 'image'

    def __init__(self, image_url, *, title: str = None, alt_text: str = None, **kwargs):
        super(ImageBlock, self).__init__(**kwargs)

        self.image_url = image_url

        self.title = title
        self.alt_text = alt_text or image_url

    def to_dict(self):
        data = super(ImageBlock, self).to_dict()

        data['image_url'] = self.image_url

        if self.title:
            data['title'] = {
                'type': self.content_type,
                'text': self.title,
            }

        if self.alt_text:
            data['alt_text'] = self.alt_text

        return data

    def accept(self, converter):
        return converter.convert_image_block(self)


class ContextBlockTextElement(BaseBlockField):

    def __init__(self, text, **kwargs):
        super(ContextBlockTextElement, self).__init__(**kwargs)

        self.text = text

    def to_dict(self):
        data = super(ContextBlockTextElement, self).to_dict()

        data['text'] = self.text
        data['type'] = self.content_type

        return data

    def accept(self, converter):
        return converter.convert_context_block_text_element(self)


class ContextBlockImageElement(BaseBlockField):
    __type__ = 'image'

    def __init__(self, image_url, alt_text: str = None):
        super(ContextBlockImageElement, self).__init__()

        self.image_url = image_url
        self.alt_text = alt_text

    def to_dict(self):
        data = super(ContextBlockImageElement, self).to_dict()

        data['image_url'] = self.image_url

        if self.alt_text:
            data['alt_text'] = self.alt_text

        return data

    def accept(self, converter):
        return converter.convert_context_block_image_element(self)


class ContextBlock(BaseBlock):
    __type__ = 'context'

    TextElement = ContextBlockTextElement
    ImageElement = ContextBlockImageElement

    def __init__(self, elements: List[Union[ContextBlockTextElement, ContextBlockImageElement]], **kwargs):
        super(ContextBlock, self).__init__(**kwargs)

        self.elements = elements

    def to_dict(self):
        data = super(ContextBlock, self).to_dict()

        data['elements'] = [e.to_dict() for e in self.elements]

        return data

    def accept(self, converter):
        return converter.convert_context_block(self)


class ButtonBlock(BaseBlock):
    __type__ = 'button'

    def __init__(self, text: str, action_id: str, value: str, style: str = None,  **kwargs):
        super(ButtonBlock, self).__init__(**kwargs)

        self.text = text
        self.action_id = action_id
        self.value = value
        self.style = style

    def to_dict(self):
        data = super(ButtonBlock, self).to_dict()

        data['action_id'] = self.action_id
        data['value'] = self.value
        data['text'] = {
            'type': 'plain_text',
            'text': self.text,
        }
        if self.style is not None:
            data['style'] = self.style

        return data

    def accept(self, converter):
        return converter.convert_button_block(self)


class ActionsBlock(BaseBlock):
    __type__ = 'actions'

    def __init__(self, elements: List[ButtonBlock], **kwargs):
        super(ActionsBlock, self).__init__(**kwargs)

        self.elements = elements

    def to_dict(self):
        data = super(ActionsBlock, self).to_dict()

        data['elements'] = [e.to_dict() for e in self.elements]

        return data

    def accept(self, converter):
        return converter.convert_actions_block(self)
