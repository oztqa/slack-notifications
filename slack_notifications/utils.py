import string
import random

from slack_notifications.constants import COLOR_MAP


def _random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def init_color(name, code):
    COLOR_MAP[name] = code
