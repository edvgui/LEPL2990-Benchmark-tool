from benchmark.procedure.generic import Generic
import benchmark.api.api_docker as docker
import benchmark.api.api_kata as kata
import benchmark.api.api_podman as podman
import benchmark.api.api_lxc as lxc
import benchmark.api.api_runc as runc
import time


class Network(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Network'

    def response_len(self):
        return 1

    def response_legend(self):
        return ["Ping"]

    def docker_alpine(self):
        try:
            response, _ = docker.run("alpine-network", ["--rm"], [])
        except docker.DockerApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (docker_alpine): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]

    def docker_centos(self):
        try:
            response, _ = docker.run("centos-network", ["--rm"], [])
        except docker.DockerApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (docker_alpine): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]

    def podman(self):
        try:
            response, _ = podman.run("alpine-network", ["--rm"], [])
        except podman.PodmanApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (podman): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]

    def lxc(self):
        container, launching_time = lxc.launch("alpine-network", ["-e"])
        for i in range(0, 10):
            try:
                response, _ = lxc.exec(container, ["./ping.sh", "10"])
            except lxc.LXCApiException:
                pass
            else:
                if '=' not in response:
                    print('Error (lxc): wrong response: ' + response)
                    return -1
                else:
                    lxc.stop(container)
                    return [float(response.split(" ")[3].split("/")[1]) / 1000]
            time.sleep(1)
        lxc.stop(container)
        print('Error (lxc): maximum retry reached')
        return -1

    def runc(self):
        container, _ = runc.create("alpine-network")
        try:
            response, _ = runc.run(container, [])
        except podman.PodmanApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (runc): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]
        finally:
            runc.clean(container)

    def firecracker(self):
        return 0

    def kata(self):
        try:
            response, _ = kata.run("alpine-network", ["--rm"], [])
        except kata.KataApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (kata): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]
