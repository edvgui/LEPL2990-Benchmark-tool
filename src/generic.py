import subprocess
from abc import ABC, abstractmethod
from threading import Thread


class Generic(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def ping(self, log=False):
        pass

    @abstractmethod
    def launch_big(self, sync=True, log=False):
        pass

    @abstractmethod
    def launch_read(self, log=False):
        pass

    @abstractmethod
    def launch_write(self, log=False):
        pass

    @abstractmethod
    def launch_one(self, sync=True, log=False):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def launch_many(self, number, sync=True, log=False):
        threads = []
        for i in range(0, number):
            thread = Thread(target=self.launch_one, args=(sync, log,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()