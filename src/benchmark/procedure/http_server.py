import os
import subprocess
import pycurl
import time
from io import BytesIO

from benchmark.procedure.generic import Generic
import benchmark.api.api_docker as docker
import benchmark.api.api_kata as kata
import benchmark.api.api_podman as podman
import benchmark.api.api_lxc as lxc
import benchmark.api.api_runc as runc


def server_get(url, timeout=10):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)

    tic = time.time()
    done = False
    while not done and time.time() < tic + timeout:
        try:
            c.perform()
            done = True
        except pycurl.error:
            pass
    toc = time.time()

    hw = buffer.getvalue()
    response = hw.decode('iso-8859-1')
    if 'Hello World' not in response:
        print("Error: wrong response: " + response)
        return -1
    c.close()
    return toc - tic


class HttpServer(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Http server'

    def response_len(self):
        return 3

    def docker_alpine(self):
        address = "127.0.0.1:3000"
        container, creation = docker.create("alpine-http-server", ["--rm", "-p", address + ":80"], [])
        _, start = docker.start(container, attach=False)
        result = server_get("http://" + address)
        docker.stop(container)
        return [creation, creation + start, creation + start + result] if result != -1 else -1

    def docker_centos(self):
        address = "127.0.0.1:3001"
        container, creation = docker.create("centos-http-server", ["--rm", "-p", address + ":80"], [])
        _, start = docker.start(container, attach=False)
        result = server_get("http://" + address)
        docker.stop(container)
        return [creation, creation + start, creation + start + result] if result != -1 else -1

    def podman(self):
        address = "127.0.0.1:3002"
        container, creation = podman.create("alpine-http-server", ["--rm", "-p", address + ":80"], [])
        _, start = podman.start(container, attach=False)
        result = server_get("http://" + address)
        podman.stop(container)
        return [creation, creation + start, creation + start + result] if result != -1 else -1

    def lxc(self):
        address = "127.0.0.1:3003"
        container, creation = lxc.init("alpine-http-server", ["-e"], [])
        device = "device-" + container
        configuration = lxc.config_proxy_add(container, device, address)
        start = lxc.start(container)
        response, execution = lxc.exec(container, ["/usr/sbin/lighttpd", "-f", "/etc/lighttpd/lighttpd.conf"])
        result = server_get("http://" + address)
        lxc.config_proxy_rm(container, device)
        lxc.stop(container)
        return [creation + configuration, creation + configuration + start + execution,
                creation + configuration + start + result] if result != -1 else -1

    def runc(self):
        address = "127.0.0.1:3004"
        container, creation_duration = runc.create("alpine-http-server")

        directory = os.path.dirname(os.path.abspath(__file__))
        runc_folder = os.path.join(directory, '../../resources/runc')
        path = os.path.join(runc_folder, 'run')

        tic = time.time()
        proc = subprocess.Popen([path, "-p", address + ":80/tcp", "-d", container],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        result = -1
        for line in iter(proc.stdout.readline, b''):
            if line.decode('utf-8').strip() == container:
                result = server_get("http://" + address)
                toc = time.time()
                if result != -1:
                    result = toc - tic
                runc.stop(container)
                runc.clean(container)

        if result == -1:
            print("error")
            return -1

        return [creation_duration, creation_duration, result + creation_duration]

    def firecracker(self):
        return [0, 0, 0]

    def kata(self):
        address = "127.0.0.1:3006"
        container, creation = kata.create("alpine-http-server", ["--rm", "-p", address + ":80"], [])
        _, start = kata.start(container, attach=False)
        result = server_get("http://" + address)
        kata.stop(container)
        return [creation, creation + start, creation + start + result] if result != -1 else -1
