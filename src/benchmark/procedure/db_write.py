from procedure.generic import Generic
import api.api_docker as docker
import api.api_firecracker as firecracker
import api.api_kata as kata
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
        return 2

    def response_legend(self):
        return ["Create", "Start + Exec"]

    def docker_alpine(self):
        container, creation = docker.create("alpine-db-" + self.size + "-write", ["--rm"], [])
        response, execution = docker.start(container)
        if 'Done' not in response:
            print('Error (docker_alpine): wrong response: ' + response)
            return -1
        return [creation, creation + execution]

    def docker_centos(self):
        container, creation = docker.create("centos-db-" + self.size + "-write", ["--rm"], [])
        response, execution = docker.start(container)
        if 'Done' not in response:
            print('Error (docker_centos): wrong response: ' + response)
            return -1
        return [creation, creation + execution]

    def podman(self):
        container, creation = podman.create("alpine-db-" + self.size + "-write", ["--rm"], [])
        response, execution = podman.start(container)
        if 'Done' not in response:
            print('Error (podman): wrong response: ' + response)
            return -1
        return [creation, creation + execution]

    def lxc(self):
        container, creation = lxc.init("alpine-db-" + self.size + "-write", ["-e"])
        start = lxc.start(container)
        response, execution_time = lxc.exec(container, ["./sqlite.sh", "tpcc.db", "write.sqlite"])
        if 'Done' not in response:
            print("Error (lxc): wrong response: " + response)
            return -1
        lxc.stop(container)
        return [creation, creation + start + execution_time]

    def runc(self):
        container, creation_time = runc.create("alpine-db-" + self.size + "-write")
        response, execution_time = runc.run(container, ["-o"])
        if 'Done' not in response:
            print("Error (runc): wrong response: " + response)
            return -1
        runc.clean(container)
        return [creation_time, creation_time + execution_time]

    def firecracker(self):
        container, creation = firecracker.create("alpine-db-" + self.size + "-write", ["--rm"])
        start = firecracker.start(container)
        response, execution = firecracker.exec(container, ["/run/run.sh", "/run/tpcc.db", "/run/write.sqlite"])
        if 'Done' not in response:
            print("Error (firecracker): wrong response: " + response)
        firecracker.stop(container)
        return [creation, creation + start + execution]

    def kata(self):
        container, creation = kata.create("alpine-db-" + self.size + "-write", ["--rm"])
        response, execution = kata.start(container)
        if 'Done' not in response:
            print('Error (kata): wrong response: ' + response)
            return -1
        return [creation, creation + execution]
