from procedure.generic import Generic
import api.api_docker as docker
import api.api_firecracker as firecracker
import api.api_kata as kata
import api.api_podman as podman
import api.api_lxc as lxc
import api.api_runc as runc


class HelloWorld(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Hello World'

    def response_len(self):
        return 2

    def response_legend(self):
        return ["Create", "Start + Exec"]

    def docker_alpine(self):
        container, creation = docker.create("alpine-hello-world", ["--rm"], [])
        response, execution = docker.start(container)
        if 'Hello World' not in response:
            print('Error (docker_alpine): wrong response: ' + response)
        return [creation, creation + execution]

    def docker_centos(self):
        container, creation = docker.create("centos-hello-world", ["--rm"], [])
        response, execution = docker.start(container)
        if 'Hello World' not in response:
            print('Error (docker_centos): wrong response: ' + response)
        return [creation, creation + execution]

    def podman(self):
        container, creation = podman.create("alpine-hello-world", ["--rm"], [])
        response, execution = podman.start(container)
        if 'Hello World' not in response:
            print('Error (podman): wrong response: ' + response)
        return [creation, creation + execution]

    def lxc(self):
        container, creation = lxc.init("alpine-hello-world", ["-e"])
        start = lxc.start(container)
        response, execution_time = lxc.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print("Error (lxc): wrong response: " + response)
        lxc.stop(container)
        return [creation, creation + start + execution_time]

    def runc(self):
        container, creation_time = runc.create("alpine-hello-world")
        response, execution_time = runc.run(container, ["-o"])
        if 'Hello World' not in response:
            print("Error (runc): wrong response: " + response)
        runc.clean(container)
        return [creation_time, creation_time + execution_time]

    def firecracker(self):
        container, creation = firecracker.create("alpine-hello-world", ["--rm"])
        start = firecracker.start(container)
        response, execution = firecracker.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print("Error (firecracker): wrong response: " + response)
        firecracker.stop(container)
        return [creation, creation + start + execution]

    def kata(self):
        container, creation = kata.create("alpine-hello-world", ["--rm"])
        response, execution = kata.start(container)
        if 'Hello World' not in response:
            print('Error (kata): wrong response: ' + response)
        return [creation, creation + execution]
