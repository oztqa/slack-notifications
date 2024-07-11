from typing import List

from notifications.fields.blocks import (
    HeaderBlock,
    SimpleTextBlock,
    SimpleTextBlockField,
    DividerBlock,
    ImageBlock,
    ContextBlock,
    ContextBlockTextElement,
    ContextBlockImageElement,
    ActionsBlock,
    ButtonBlock
)

from notifications.fields.attachments import Attachment, AttachmentField


class MattermostConverter:
    def __init__(self, *, header_level: int = 4):
        self.result = ''
        self._level = header_level

    def fields_to_table(self, fields: List[SimpleTextBlockField]):
        header = '| |'
        separator = '|:---|---:|'

        table_rows = []
        for i in range(0, len(fields), 2):
            row = fields[i:i + 2]
            table_rows.append('|'+'|'.join(map(self.convert_simple_text_block_field, row))+'|')

        return '\n'.join([header, separator] + table_rows)

    def convert_header_block(self, block: HeaderBlock):
        sign = '#'
        self.result += f'\n{sign * self._level} {block.text}'

    def convert_simple_text_block(self, block: SimpleTextBlock):
        self.result += f'\n{block.text}\n\n{self.fields_to_table(block.fields)}\n' if block.fields else f'\n{block.text}\n'

    def convert_simple_text_block_field(self, block_field: SimpleTextBlockField):
        return f'{block_field.text}'

    def convert_divider_block(self, block: DividerBlock):
        self.result += '\n---\n'

    def convert_image_block(self, block: ImageBlock):
        pass

    def convert_context_block(self, block: ContextBlock):
        pass

    def convert_context_block_image_element(self, block_element: ContextBlockImageElement):
        pass

    def convert_context_block_text_element(self, block_element: ContextBlockTextElement):
        pass

    def convert_actions_block(self, block: ActionsBlock):
        pass

    def convert_button_block(self, block: ButtonBlock):
        pass

    def convert_attachments_block(self, attachment: Attachment):
        pass
