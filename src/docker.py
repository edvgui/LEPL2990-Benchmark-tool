import subprocess

from src.generic import Generic


class Docker(Generic):

    def __init__(self):
        super().__init__()

    def ping(self, log=False):
        args = ["docker", "run", "--rm", "network", "/run.sh"]
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)
        vals = output.split(" ")
        print(vals)
        return vals[3].split('/')

    def launch_big(self, sync=True, log=False):
        args = ["docker", "run", "--rm"]
        if not sync:
            args.append("-d")

        args.extend(["mondial-read", "/bin/echo", "Hello World"])
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)

    def launch_read(self, log=False):
        args = ["docker", "run", "--rm", "mondial-read", "/run.sh"]
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)

    def launch_write(self, log=False):
        args = ["docker", "run", "--rm", "mondial-write", "/run.sh"]
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)

    def launch_one(self, sync=True, log=False):
        args = ["docker", "run", "--rm"]
        if not sync:
            args.append("-d")

        args.extend(["alpine:latest", "/bin/echo", "Hello World"])
        output = subprocess.run(args, stdout=subprocess.PIPE)
        if log:
            print(output)

    def get_name(self):
        return 'Docker'
