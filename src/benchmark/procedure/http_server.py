import os
import subprocess
import pycurl
import time
from io import BytesIO

from procedure.generic import Generic
import api.api_docker as docker
import api.api_podman as podman
import api.api_lxd as lxc
import api.api_contingious as contingious


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
        return 4

    def response_legend(self):
        return ["Create", "Start", "Exec", "1st response"]

    def docker(self, image, runtime):
        address = "127.0.0.1:3000"
        options = ["--rm", "-p", address + ":80"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        container, creation = docker.create("edvgui/%s-http-server" % image, options=options)
        _, start = docker.start(container)
        _, execution = docker.exec(container, ["/usr/sbin/lighttpd", "-f", "/etc/lighttpd/lighttpd.conf"])
        result = server_get("http://" + address)
        docker.kill(container)
        return [creation, creation + start, creation + start + execution,
                creation + start + execution + result] if result != -1 else -1

    def podman(self, image, runtime):
        address = "127.0.0.1:3000"
        options = ["-p", address + ":80"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        container, creation = podman.create("edvgui/%s-http-server" % image, options=options)
        _, start = podman.start(container)
        _, execution = podman.exec(container, ["/usr/sbin/lighttpd", "-f", "/etc/lighttpd/lighttpd.conf"])
        result = server_get("http://" + address)
        podman.kill(container)
        podman.rm(container)
        return [creation, creation + start, creation + start + execution,
                creation + start + execution + result] if result != -1 else -1

    def lxd(self, image, runtime):
        address = "127.0.0.1:3000"
        container, creation = lxc.init("edvgui/%s-http-server" % image, ["-e", "--profile", "default", "--profile",
                                                                         "online", "--profile", "server-3000"])
        start = lxc.start(container)
        response, execution = lxc.exec(container, ["/usr/sbin/lighttpd", "-f", "/etc/lighttpd/lighttpd.conf"])
        result = server_get("http://" + address)
        lxc.kill(container)
        return [creation, creation + start, creation + start + execution,
                creation + start + execution + result] if result != -1 else -1

    def contingious(self, image, runtime):
        address = "127.0.0.1:3000"
        container, creation = contingious.create("edvgui/%s-http-server" % image, network=True, port=(address + ":80/tcp"))
        _, start = contingious.start(container, network=True)
        response, execution = contingious.exec(container, "/usr/sbin/lighttpd -f /etc/lighttpd/lighttpd.conf", network=True)
        result = server_get("http://" + address)
        contingious.kill(container)
        contingious.clean(container, network=True)
        return [creation, creation + start, creation + start + execution,
                creation + start + execution + result] if result != -1 else -1
