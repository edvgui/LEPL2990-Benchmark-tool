from abc import ABC, abstractmethod


class Generic(ABC):

    def __init__(self):
        super().__init__()
        self.functions = {
            'docker': self.docker,
            'podman': self.podman,
            'lxc': self.lxc,
            'contingious': self.contingious
        }

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def response_len(self):
        pass

    @abstractmethod
    def response_legend(self):
        pass

    @abstractmethod
    def docker(self, image, runtime):
        pass

    @abstractmethod
    def podman(self, image, runtime):
        pass

    @abstractmethod
    def lxc(self, image, runtime):
        pass

    @abstractmethod
    def contingious(self, image, runtime):
        pass
