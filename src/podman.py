import subprocess

from src.generic import Generic


class Podman(Generic):

    def __init__(self):
        super().__init__()

    def ping(self, log=False):
        args = ["podman", "run", "--rm", "network", "/run.sh"]
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)
        vals = output.split(" ")
        print(vals)
        return vals[3].split('/')

    def launch_big(self, sync=True, log=False):
        args = ["podman", "run", "--rm"]
        if not sync:
            args.append("-d")

        args.extend(["mondial-read", "/bin/echo", "Hello World"])
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)

    def launch_read(self, log=False):
        args = ["podman", "run", "--rm", "mondial-read", "/run.sh"]
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)

    def launch_write(self, log=False):
        args = ["podman", "run", "--rm", "mondial-write", "/run.sh"]
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)

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
