from src.procedure.generic import Generic
import src.api.api_docker as docker
import src.api.api_podman as podman
import src.api.api_lxc as lxc


class MondialWrite(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Mondial write'

    def docker_alpine(self):
        response, duration = docker.run("alpine-mondial-write", ["--rm"], [])
        if 'Done' not in response:
            print('Error: wrong response: ' + response)
        return duration

    def docker_centos(self):
        response, duration = docker.run("centos-mondial-write", ["--rm"], [])
        if 'Done' not in response:
            print('Error: wrong response: ' + response)
        return duration

    def podman(self):
        response, duration = podman.run("alpine-mondial-write", ["--rm"], [])
        if 'Done' not in response:
            print('Error: wrong response: ' + response)
        return duration

    def lxc(self):
        container, launching_time = lxc.launch("alpine-mondial-write", ["-e"])
        response, execution_time = lxc.exec(container, ["./write.sh"])
        if 'Done' not in response:
            print("Error: wrong response: " + response)
        lxc.stop(container)
        return launching_time + execution_time

    def runc(self):
        return 0

    def firecracker(self):
        return 0

    def kata(self):
        return 0
