from src.procedure.generic import Generic
import src.api.api_docker as docker
import src.api.api_podman as podman
import src.api.api_lxc as lxc
import pycurl
import time
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor


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
        with ThreadPoolExecutor(max_workers=1) as executor:
            thread = executor.submit(server_get, 'http://' + address)
            container, duration = docker.run("alpine-http-server", ["--rm", "-d", "-p", address + ":80"], [])
            result = thread.result()
            docker.stop(container)
            return result

    def docker_centos(self):
        address = "127.0.0.1:3001"
        with ThreadPoolExecutor(max_workers=1) as executor:
            thread = executor.submit(server_get, 'http://' + address)
            container, duration = docker.run("centos-http-server", ["--rm", "-d", "-p", address + ":80"], [])
            result = thread.result()
            docker.stop(container)
            return result

    def podman(self):
        address = "127.0.0.1:3002"
        with ThreadPoolExecutor(max_workers=1) as executor:
            thread = executor.submit(server_get, 'http://' + address)
            container, duration = podman.run("alpine-http-server", ["--rm", "-d", "-p", address + ":80"], [])
            result = thread.result()
            podman.stop(container)
            return result

    def lxc(self):
        address = "127.0.0.1:3003"
        device = "my-device"
        with ThreadPoolExecutor(max_workers=1) as executor:
            thread = executor.submit(server_get, 'http://' + address)
            container, duration = lxc.launch("alpine-http-server", ["-e"], [])
            lxc.config_proxy_add(container, device, address)
            result = thread.result()
            lxc.config_proxy_rm(container, device)
            lxc.stop(container)
            return result

    def runc(self):
        return 0

    def firecracker(self):
        return 0

    def kata(self):
        return 0
