from typing import Protocol


class InterfaceMessage(Protocol):

    def send_to_thread(self, **kwargs):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def upload_file(self, file, **kwargs):
        pass

    def add_reaction(self, name, raise_exc=False):
        pass

    def remove_reaction(self, name, raise_exc=False):
        pass


class InterfaceClient(Protocol):
    def send_notification(self) -> InterfaceMessage:
        pass

    def upload_file(self):
        pass
