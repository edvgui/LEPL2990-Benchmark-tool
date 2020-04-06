from benchmark.procedure.generic import Generic
import benchmark.api.api_docker as docker
import benchmark.api.api_kata as kata
import benchmark.api.api_podman as podman
import benchmark.api.api_lxc as lxc
import benchmark.api.api_runc as runc


class WarmUp(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Warm up'

    def response_len(self):
        return 1

    def response_legend(self):
        return ["Run"]

    def docker_alpine(self):
        response, duration = docker.run("alpine-hello-world", ["--rm"], [])
        if 'Hello World' not in response:
            print('Error (docker_alpine): wrong response: ' + response)
        return [duration]

    def docker_centos(self):
        response, duration = docker.run("centos-hello-world", ["--rm"], [])
        if 'Hello World' not in response:
            print('Error (docker_centos): wrong response: ' + response)
        return [duration]

    def podman(self):
        response, duration = podman.run("alpine-hello-world", ["--rm"], [])
        if 'Hello World' not in response:
            print('Error (podman): wrong response: ' + response)
        return [duration]

    def lxc(self):
        container, launching_time = lxc.launch("alpine-hello-world", ["-e"])
        response, execution_time = lxc.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print("Error (lxc): wrong response: " + response)
        lxc.stop(container)
        return [launching_time + execution_time]

    def runc(self):
        container, creation_time = runc.create("alpine-hello-world")
        response, execution_time = runc.run(container, ["-o"])
        if 'Hello World' not in response:
            print("Error (runc): wrong response: " + response)
        runc.clean(container)
        return [creation_time + execution_time]

    def firecracker(self):
        return [0]

    def kata(self):
        response, duration = kata.run("alpine-hello-world", ["--rm"], [])
        if 'Hello World' not in response:
            print('Error (kata): wrong response: ' + response)
        return [duration]
