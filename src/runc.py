import subprocess
from random import randint
from src.generic import Generic


class RunC(Generic):

    def ping(self, log=False):
        pass

    def launch_big(self, sync=True, log=False):
        pass

    def launch_read(self, log=False):
        pass

    def launch_write(self, log=False):
        pass

    def __init__(self):
        super().__init__()

    def launch_one(self, sync=True, log=False):
        args = ["runc", "run"]
        if not sync:
            args.append("-d")

        args.extend(["-b", "../resources/runc/hello-world", str(randint(1000000, 9999999))])
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)

    def get_name(self):
        return 'runC'
