from src.procedure.generic import Generic
import src.api.api_docker as docker
import src.api.api_podman as podman
import src.api.api_lxc as lxc
import src.api.api_runc as runc


class MondialRead(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Mondial read'

    def docker_alpine(self):
        response, duration = docker.run("alpine-mondial-read", ["--rm"], [])
        if 'Done' not in response:
            print('Error (docker_alpine): wrong response: ' + response)
        return duration

    def docker_centos(self):
        response, duration = docker.run("centos-mondial-read", ["--rm"], [])
        if 'Done' not in response:
            print('Error (docker_centos): wrong response: ' + response)
        return duration

    def podman(self):
        response, duration = podman.run("alpine-mondial-read", ["--rm"], [])
        if 'Done' not in response:
            print('Error (podman): wrong response: ' + response)
        return duration

    def lxc(self):
        container, launching_time = lxc.launch("alpine-mondial-read", ["-e"])
        response, execution_time = lxc.exec(container, ["./sqlite.sh", "mondial-orig.db", "read.sqlite"])
        if 'Done' not in response:
            print("Error (lxc): wrong response: " + response)
        lxc.stop(container)
        return launching_time + execution_time

    def runc(self):
        status, container, creation_time = runc.create("alpine-mondial-read")
        status, response, execution_time = runc.run(container)
        if 'Done' not in response:
            print("Error (runc): wrong response: " + response)
        status, response, deletion_time = runc.clean(container)
        return creation_time + execution_time

    def firecracker(self):
        return 0

    def kata(self):
        return 0
