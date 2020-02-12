import subprocess

from generic import Generic


class Podman(Generic):

    def __init__(self):
        super().__init__()

    def launch_one(self, sync=True, log=False):
        args = ["podman", "run", "--rm"]
        if not sync:
            args.append("-d")

        args.extend(["docker.io/library/alpine", "/bin/echo", "Hello World"])
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)

    def get_name(self):
        return 'Podman'
