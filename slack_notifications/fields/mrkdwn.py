from typing import Iterable


def bold(text):
    return f'*{str(text)}*'


def italic(text):
    return f'_{str(text)}_'


def strike(text):
    return f'~{str(text)}~'


def code_block(text):
    return f'`{str(text)}`'


def multi_line_code_block(text):
    return f'```{str(text)}```'


def block_quotes(text):
    return f'\n>{str(text)}\n'


def list_items(itr: Iterable):
    return '\n'.join([f'• {str(item)}' for item in itr]) + '\n'


def link(url, text):
    return f'<{url}|{str(text)}>'


def user_mention(user_id):
    return f'<@{user_id}>'


def channel_mention(channel):
    return f'<#{channel}>'
