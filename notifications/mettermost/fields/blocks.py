from typing import List

from notifications.interfaces.fields import ConvertibleObject


class BaseBlock(ConvertibleObject):
    def __init__(self):
        super(BaseBlock, self).__init__()

    def convert(self):
        return str(self)

    def __str__(self):
        raise NotImplementedError(
            'Object "{}" does not implemented "__str__" method'.format(self.__class__.__name__),
        )


class HeaderBlock(BaseBlock):
    sign = '#'

    def __init__(self, text, *, level=3, header_id=None):
        super(HeaderBlock, self).__init__()
        self._text = text
        self._level = level
        self._header_id = header_id

    def __str__(self):
        return f'\n{self.sign * self._level} {self._text}{self.header_id}\n'

    @property
    def header_id(self):
        return ' {#%s}' % self._header_id if self._header_id else ''


class SimpleTextBlockField(BaseBlock):

    def __init__(self, text: str):
        super(SimpleTextBlockField, self).__init__()

        self.text = text

    def __str__(self):
        return f'{self.text}'


class SimpleTextBlock(BaseBlock):

    Field = SimpleTextBlockField

    def __init__(self, text: str, *, fields: List[SimpleTextBlockField] = None):
        super(SimpleTextBlock, self).__init__()

        self.text = text
        self._fields = fields

    def __str__(self):
        return f'\n{self.text}\n\n{self.fields_to_table()}\n' if self._fields else f'\n{self.text}\n'

    def fields_to_table(self):
        header = '| |'
        separator = '|:---|---:|'

        table_rows = []
        for i in range(0, len(self._fields), 2):
            row = self._fields[i:i + 2]
            table_rows.append('|'+'|'.join(map(str, row))+'|')

        return '\n'.join([header, separator] + table_rows)


class DividerBlock:
    def __str__(self):
        return f'\n---\n'


class MultiCodeBlock(BaseBlock):
    def __init__(self, code: str, *, language=None):
        super(MultiCodeBlock, self).__init__()
        self.code = code
        self._language = language

    def __str__(self):
        return f'\n```{self._language or ""}\n{self.code}\n```'


class TableBlock(BaseBlock):
    def __init__(self, column_names, items):
        super(TableBlock, self).__init__()
        self._column_names = column_names
        self._columns_count = len(column_names)
        self.items = items

    def _create_table(self):
        if len(self.items) % self._columns_count != 0:
            raise ValueError('Items must divisible by the number of columns')

        header = ' | '.join(self._column_names)
        separator = ' | '.join(['---'] * self._columns_count)

        table_rows = []
        for i in range(0, len(self.items), self._columns_count):
            row = self.items[i:i + self._columns_count]
            table_rows.append(' | '.join(map(str, row)))

        table = '\n'.join([header, separator] + table_rows)

        return table

    def __str__(self):
        return f'{self._create_table()}'
