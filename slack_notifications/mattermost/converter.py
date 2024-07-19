from typing import List

from slack_notifications.fields import (
    BaseBlock,
    HeaderBlock,
    SimpleTextBlock,
    SimpleTextBlockField,
    DividerBlock,
    ImageBlock,
    ContextBlock,
    ContextBlockTextElement,
    ContextBlockImageElement,
    ActionsBlock,
    ButtonBlock,
    Attachment
)


class MattermostConverter:
    def __init__(self, *, header_level: int = 4, blocks: List[BaseBlock] = None):
        self.message = ''
        self._level = header_level
        self._blocks = blocks or []
        self.attachments_result = []

        self.block_handlers: dict[type[BaseBlock], callable] = {
            HeaderBlock: self.convert_header_block,
            SimpleTextBlock: self.convert_simple_text_block,
            DividerBlock: self.convert_divider_block,
            ImageBlock: self.convert_image_block,
            ContextBlock: self.convert_context_block,
        }

    def convert(self, blocks: List[BaseBlock]):
        if not blocks:
            return

        attachment = Attachment(color='gray')
        attachment_data = attachment.to_dict()
        attachment_data['actions'] = []

        for block in blocks:
            block_handler = self.block_handlers.get(type(block))
            if block_handler:
                block_handler(block)

            if isinstance(block, ActionsBlock):
                attachment_data['actions'] += self.convert_actions_block(block)

        if 'actions' in attachment_data:

            self.attachments_result.append(attachment_data)

    def fields_to_table(self, fields: List[SimpleTextBlockField]):
        header = '| |'
        separator = '|:---|---:|'

        table_rows = []
        for i in range(0, len(fields), 2):
            row = fields[i:i + 2]
            table_rows.append('|' + '|'.join(map(lambda v: str(v.text), row)) + '|')

        return '\n'.join([header, separator] + table_rows)

    def convert_header_block(self, block: HeaderBlock):
        sign = '#'
        self.message += f'\n{sign * self._level} {block.text}'

    def convert_simple_text_block(self, block: SimpleTextBlock):
        self.message += f'\n{block.text}\n\n{self.fields_to_table(block.fields)}\n'\
            if block.fields else f'\n{block.text}\n'

    def convert_divider_block(self, block: DividerBlock):
        self.message += '\n---\n'

    def convert_image_block(self, block: ImageBlock):
        self.message += f'\n![{block.title}]({block.image_url}\n)'

    def convert_context_block(self, block: ContextBlock):
        self.message += '\n'
        for element in block.elements:
            if isinstance(element, ContextBlockTextElement):
                self.message += f' *{element.text}* '
            if isinstance(element, ContextBlockImageElement):
                self.message += f' ![{element.alt_text}]({element.image_url} =30) '
        self.message += '\n'

    def convert_actions_block(self, block: ActionsBlock):
        data = []
        for element in block.elements:
            if isinstance(element, ButtonBlock):
                data.append(self.convert_button_block(element))
        return data

    def convert_button_block(self, block: ButtonBlock):
        data = {
            'id': block.action_id,
            'type': block.__type__,
            'name': block.text,
            'integration': {
                'context': {
                    'value': block.value
                }
            }
        }
        if block.style is not None:
            data['style'] = block.style

        return data
