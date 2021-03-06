from random import random

from procedure.generic import Generic


class Example(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Example'

    def response_len(self):
        return 3

    def response_legend(self):
        return ["1", "2", "3"]

    def docker(self, image, runtime):
        results = []
        acc = 0
        for _ in range(0, self.response_len()):
            acc += random()
            results.append(acc)
        return results

    def podman(self, image, runtime):
        results = []
        acc = 0
        for _ in range(0, self.response_len()):
            acc += random()
            results.append(acc)
        return results

    def lxd(self, image, runtime):
        results = []
        acc = 0
        for _ in range(0, self.response_len()):
            acc += random()
            results.append(acc)
        return results

    def contingious(self, image, runtime):
        results = []
        acc = 0
        for _ in range(0, self.response_len()):
            acc += random()
            results.append(acc)
        return results
