import subprocess

from src.generic import Generic


class Inginious(Generic):

    def __init__(self):
        super().__init__()

    def launch_one(self, sync=True, log=False):
        args = ["docker", "run", "--rm"]
        if not sync:
            args.append("-d")

        args.extend(["centos:7", "/bin/echo", "Hello World"])
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)
        pass

    def get_name(self):
        return 'Inginious'
