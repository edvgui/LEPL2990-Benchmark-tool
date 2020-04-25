from procedure.generic import Generic
import api.api_docker as docker
import api.api_firecracker as firecracker
import api.api_qemu as qemu
import api.api_podman as podman
import api.api_lxc as lxc
import api.api_runc as runc


class DatabaseWrite(Generic):

    def __init__(self, size='xl'):
        super().__init__()
        if size not in ['xs', 'sm', 'md', 'lg', 'xl']:
            self.size = 'xl'
        else:
            self.size = size

    def name(self):
        return 'Database write ' + self.size

    def response_len(self):
        return 3

    def response_legend(self):
        return ["Create", "Start", "Exec"]

    def docker_alpine(self):
        container, creation = docker.create("edvgui/alpine-db-" + self.size + "-write", ["--rm"])
        _, start = docker.start(container)
        response, execution = docker.exec(container, ["/run/run.sh", "/home/tpcc.db", "/run/write.sqlite"])
        if 'Done' not in response:
            print("Error (docker_alpine): wrong response: " + response)
        docker.kill(container)
        return [creation, creation + start, creation + start + execution]

    def docker_centos(self):
        container, creation = docker.create("edvgui/centos-db-" + self.size + "-write", ["--rm"])
        _, start = docker.start(container)
        response, execution = docker.exec(container, ["/run/run.sh", "/home/tpcc.db", "/run/write.sqlite"])
        if 'Done' not in response:
            print("Error (docker_centos): wrong response: " + response)
        docker.kill(container)
        return [creation, creation + start, creation + start + execution]

    def podman(self):
        container, creation = podman.create("edvgui/alpine-db-" + self.size + "-write", ["--rm"])
        _, start = podman.start(container)
        response, execution = podman.exec(container, ["/run/run.sh", "/home/tpcc.db", "/run/write.sqlite"])
        if 'Done' not in response:
            print("Error (podman): wrong response: " + response)
        podman.kill(container)
        return [creation, creation + start, creation + start + execution]

    def lxc(self):
        container, creation = lxc.init("alpine-db-" + self.size + "-write", ["-e"])
        start = lxc.start(container)
        response, execution_time = lxc.exec(container, ["./sqlite.sh", "tpcc.db", "write.sqlite"])
        if 'Done' not in response:
            print("Error (lxc): wrong response: " + response)
            return -1
        lxc.stop(container)
        return [creation, creation + start, creation + start + execution_time]

    def runc(self):
        container, creation_time = runc.create("alpine-db-" + self.size + "-write")
        response, execution_time = runc.run(container, ["-o"])
        if 'Done' not in response:
            print("Error (runc): wrong response: " + response)
            return -1
        runc.clean(container)
        return [creation_time, creation_time + execution_time, creation_time + execution_time]

    def firecracker(self):
        container, creation = firecracker.create("edvgui/alpine-db-" + self.size + "-write", ["--rm"])
        _, start = firecracker.start(container)
        response, execution = firecracker.exec(container, ["/run/run.sh", "/home/tpcc.db", "/run/write.sqlite"])
        if 'Done' not in response:
            print("Error (firecracker): wrong response: " + response)
        firecracker.kill(container)
        return [creation, creation + start, creation + start + execution]

    def qemu(self):
        container, creation = qemu.create("edvgui/alpine-db-" + self.size + "-write", ["--rm"])
        _, start = qemu.start(container)
        response, execution = qemu.exec(container, ["/run/run.sh", "/home/tpcc.db", "/run/write.sqlite"])
        if 'Done' not in response:
            print("Error (qemu): wrong response: " + response)
        qemu.kill(container)
        return [creation, creation + start, creation + start + execution]
