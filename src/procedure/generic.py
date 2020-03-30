from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed


class Generic(ABC):

    def __init__(self):
        super().__init__()
        self.__functions = {
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
        print("Executing {0}".format(self.name()))

        for function in self.__functions:
            print("\t{0}".format(function))
            target = self.__functions[function]

            if parallelize:
                with ThreadPoolExecutor(max_workers=repetition) as executor:
                    threads = [executor.submit(target) for i in range(0, repetition)]
                    result = list(filter(lambda i: i != -1, [future.result() for future in as_completed(threads)]))
            else:
                result = list(filter(lambda i: i != -1, [target() for i in range(0, repetition)]))

            results[function] = result

        return results
