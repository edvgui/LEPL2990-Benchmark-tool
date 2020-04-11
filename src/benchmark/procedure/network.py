from procedure.generic import Generic
import api.api_docker as docker
import api.api_firecracker as firecracker
import api.api_qemu as qemu
import api.api_podman as podman
import api.api_lxc as lxc
import api.api_runc as runc
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
        container, _ = firecracker.launch("alpine-network", ["--rm"])
        try:
            response, _ = firecracker.exec(container, ["/run/run.sh"])
        except firecracker.FirecrackerApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (firecracker): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]
        finally:
            firecracker.stop(container)

    def qemu(self):
        try:
            response, _ = qemu.run("alpine-network", ["--rm"], [])
        except qemu.QemuApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (qemu): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]
