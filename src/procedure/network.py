from src.procedure.generic import Generic
import src.api.api_docker as docker
import src.api.api_podman as podman
import src.api.api_lxc as lxc


class Network(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Network'

    def docker_alpine(self):
        response, duration = docker.run("alpine-network", ["--rm"], [])
        if '=' not in response:
            print('Error: wrong response: ' + response)
            return -1
        else:
            return float(response.split(" ")[3].split("/")[1])

    def docker_centos(self):
        response, duration = docker.run("centos-network", ["--rm"], [])
        if '=' not in response:
            print('Error: wrong response: ' + response)
            return -1
        else:
            return float(response.split(" ")[3].split("/")[1])

    def podman(self):
        response, duration = podman.run("alpine-network", ["--rm"], [])
        if '=' not in response:
            print('Error: wrong response: ' + response)
            return -1
        else:
            return float(response.split(" ")[3].split("/")[1])

    def lxc(self):
        container, launching_time = lxc.launch("alpine-network", ["-e"])
        response, execution_time = lxc.exec(container, ["./ping.sh"])
        lxc.stop(container)
        if '=' not in response:
            print('Error: wrong response: ' + response)
            return -1
        else:
            return float(response.split(" ")[3].split("/")[1])

    def runc(self):
        return 0

    def firecracker(self):
        return 0

    def kata(self):
        return 0
