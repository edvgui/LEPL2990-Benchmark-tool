from src.procedure.generic import Generic
import src.api.api_docker as docker
import src.api.api_podman as podman
import src.api.api_lxc as lxc


class HelloWorld(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Hello World'

    def docker_alpine(self):
        response, duration = docker.run("alpine-hello-world", ["--rm"], [])
        if 'Hello World' not in response:
            print('Error: wrong response: ' + response)
        return duration

    def docker_centos(self):
        response, duration = docker.run("centos-hello-world", ["--rm"], [])
        if 'Hello World' not in response:
            print('Error: wrong response: ' + response)
        return duration

    def podman(self):
        response, duration = podman.run("alpine-hello-world", ["--rm"], [])
        if 'Hello World' not in response:
            print('Error: wrong response: ' + response)
        return duration

    def lxc(self):
        container, launching_time = lxc.launch("alpine-hello-world", ["-e"])
        response, execution_time = lxc.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print("Error: wrong response: " + response)
        lxc.stop(container)
        return launching_time + execution_time

    def runc(self):
        return 0

    def firecracker(self):
        return 0

    def kata(self):
        return 0
