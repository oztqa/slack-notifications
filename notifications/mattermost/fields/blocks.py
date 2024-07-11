class MultiCodeBlock:
    def __init__(self, code: str, *, language=None):
        super(MultiCodeBlock, self).__init__()
        self.code = code
        self._language = language

    def __str__(self):
        return f'\n```{self._language or ""}\n{self.code}\n```'


class TableBlock:
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
