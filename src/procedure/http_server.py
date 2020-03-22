from src.procedure.generic import Generic
import src.api.api_docker as docker
import src.api.api_podman as podman
import src.api.api_lxc as lxc
import pycurl
import time
from io import BytesIO


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

    def docker_alpine(self):
        address = "127.0.0.1:3000"
        container, duration = docker.run("alpine-http-server", ["--rm", "-d", "-p", address + ":80"], [])
        result = server_get("http://" + address)
        docker.stop(container)
        return result + duration

    def docker_centos(self):
        address = "127.0.0.1:3001"
        container, duration = docker.run("centos-http-server", ["--rm", "-d", "-p", address + ":80"], [])
        result = server_get("http://" + address)
        docker.stop(container)
        return result + duration

    def podman(self):
        address = "127.0.0.1:3002"
        container, duration = podman.run("alpine-http-server", ["--rm", "-d", "-p", address + ":80"], [])
        result = server_get("http://" + address)
        podman.stop(container)
        return result + duration

    def lxc(self):
        address = "127.0.0.1:3003"
        container, creation_duration = lxc.launch("alpine-http-server", ["-e"], [])
        device = "device-" + container
        config_duration = lxc.config_proxy_add(container, device, address)
        result = server_get("http://" + address)
        lxc.config_proxy_rm(container, device)
        lxc.stop(container)
        return result + creation_duration + config_duration

    def runc(self):
        return 0

    def firecracker(self):
        return 0

    def kata(self):
        return 0
