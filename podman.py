import subprocess

from generic import Generic


class Podman(Generic):

    def __init__(self):
        super().__init__()

    def launch_one(self, sync=True, log=False):
        args = ["podman", "run", "--rm"]
        if not sync:
            args.append("-d")

        args.extend(["registry.fedoraproject.org/fedora", "/bin/echo", "Hello World"])
        output = subprocess.run(args, capture_output=True)
        if log:
            print(output)

    def get_name(self):
        return 'Podman'
