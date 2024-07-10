from abc import ABC, abstractmethod


class ConvertibleObject(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def convert(self):
        pass
