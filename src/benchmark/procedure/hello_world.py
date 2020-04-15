from procedure.generic import Generic
import api.api_docker as docker
import api.api_firecracker as firecracker
import api.api_qemu as qemu
import api.api_podman as podman
import api.api_lxc as lxc
import api.api_runc as runc


class HelloWorld(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Hello World'

    def response_len(self):
        return 3

    def response_legend(self):
        return ["Create", "Start", "Exec"]

    def docker_alpine(self):
        container, creation = docker.create("alpine-hello-world", ["--rm"], [])
        _, start = docker.start(container)
        response, execution = docker.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print('Error (docker_alpine): wrong response: ' + response)
        docker.kill(container)
        return [creation, creation + start, creation + start + execution]

    def docker_centos(self):
        container, creation = docker.create("centos-hello-world", ["--rm"], [])
        _, start = docker.start(container)
        response, execution = docker.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print('Error (docker_centos): wrong response: ' + response)
        docker.kill(container)
        return [creation, creation + start, creation + start + execution]

    def podman(self):
        container, creation = podman.create("alpine-hello-world", ["--rm"], [])
        _, start = podman.start(container)
        response, execution = podman.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print('Error (podman_alpine): wrong response: ' + response)
        podman.kill(container)
        return [creation, creation + start, creation + start + execution]

    def lxc(self):
        container, creation = lxc.init("alpine-hello-world", ["-e"])
        start = lxc.start(container)
        response, execution_time = lxc.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print("Error (lxc): wrong response: " + response)
        lxc.stop(container)
        return [creation, creation + start, creation + start + execution_time]

    def runc(self):
        container, creation_time = runc.create("alpine-hello-world")
        response, execution_time = runc.run(container, ["-o"])
        if 'Hello World' not in response:
            print("Error (runc): wrong response: " + response)
        runc.clean(container)
        return [creation_time, creation_time + execution_time, creation_time + execution_time]

    def firecracker(self):
        container, creation = firecracker.create("alpine-hello-world", ["--rm"])
        _, start = firecracker.start(container)
        response, execution = firecracker.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print("Error (firecracker): wrong response: " + response)
        firecracker.kill(container)
        return [creation, creation + start, creation + start + execution]

    def qemu(self):
        container, creation = qemu.create("alpine-hello-world", ["--rm"], [])
        _, start = qemu.start(container)
        response, execution = qemu.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print('Error (qemu): wrong response: ' + response)
        qemu.kill(container)
        return [creation, creation + start, creation + start + execution]
