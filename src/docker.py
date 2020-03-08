import subprocess
import time
from threading import Thread

import pycurl

from src.generic import Generic
from io import BytesIO


class Docker(Generic):

    def __init__(self):
        super().__init__()

    def serve(self, log=False):
        def launch_server(return_vals):
            args = ["docker", "run", "--rm", "-d", "-p", "127.0.0.1:3000:80", "http-server",
                    "/usr/sbin/lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
            response = subprocess.run(args, stdout=subprocess.PIPE)
            return_vals.append(str(response.stdout)[2:-3])

        def stop_server(container_id):
            args = ["docker", "stop", container_id]
            subprocess.run(args, stdout=subprocess.PIPE)

        return_vals = []
        thread = Thread(target=launch_server, args=(return_vals, ))

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://127.0.0.1:3000')
        c.setopt(c.WRITEDATA, buffer)

        start = time.time()
        thread.start()

        done = False
        while not done:
            try:
                c.perform()
                done = True
            except pycurl.error:
                pass

        hw = buffer.getvalue()
        stop = time.time()
        if 'Hello World' not in hw.decode('iso-8859-1'):
            print("Bad response!")
        c.close()

        thread.join()
        stop_server(return_vals[0])

        return stop - start

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
