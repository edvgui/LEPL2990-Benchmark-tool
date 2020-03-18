from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed


class Generic(ABC):

    def __init__(self):
        super().__init__()
        self.__functions = {
            'docker_alpine': self.docker_alpine,
            'docker_centos': self.docker_centos,
            'podman': self.podman,
            'lxc': self.lxc,
            'runc': self.runc,
            'firecracker': self.firecracker,
            'kata': self.kata
        }

    @abstractmethod
    def name(self):
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

    def execute(self, repetition=5, parallelize=False):
        results = {}

        for function in self.__functions:
            target = self.__functions[function]

            if parallelize:
                with ThreadPoolExecutor(max_workers=repetition) as executor:
                    threads = [executor.submit(target) for i in range(0, repetition)]
                    result = [future.result() for future in as_completed(threads)]
            else:
                result = [target() for i in range(0, repetition)]

            results[function] = result

        return results
