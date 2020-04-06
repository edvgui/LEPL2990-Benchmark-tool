from abc import ABC, abstractmethod


class Generic(ABC):

    def __init__(self):
        super().__init__()
        self.functions = {
            'docker_alpine': self.docker_alpine,
            'podman': self.podman,
            'lxc': self.lxc,
            'runc': self.runc,
            'docker_centos': self.docker_centos,
            'firecracker': self.firecracker,
            'kata': self.kata
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
    def docker_alpine(self):
        pass

    @abstractmethod
    def docker_centos(self):
        pass

    @abstractmethod
    def podman(self):
        pass

    @abstractmethod
    def lxc(self):
        pass

    @abstractmethod
    def runc(self):
        pass

    @abstractmethod
    def firecracker(self):
        pass

    @abstractmethod
    def kata(self):
        pass
