from benchmark.procedure.generic import Generic
import benchmark.api.api_docker as docker
import benchmark.api.api_kata as kata
import benchmark.api.api_podman as podman
import benchmark.api.api_lxc as lxc
import benchmark.api.api_runc as runc


class DatabaseRead(Generic):

    def __init__(self, size='xl'):
        super().__init__()
        if size not in ['xs', 'sm', 'md', 'lg', 'xl']:
            self.size = 'xl'
        else:
            self.size = size

    def name(self):
        return 'Database read ' + self.size

    def response_len(self):
        return 2

    def response_legend(self):
        return ["Create", "Start + Exec"]

    def docker_alpine(self):
        container, creation = docker.create("alpine-db-" + self.size + "-read", ["--rm"], [])
        response, execution = docker.start(container)
        if 'Done' not in response:
            print('Error (docker_alpine): wrong response: ' + response)
            return -1
        return [creation, creation + execution]

    def docker_centos(self):
        container, creation = docker.create("centos-db-" + self.size + "-read", ["--rm"], [])
        response, execution = docker.start(container)
        if 'Done' not in response:
            print('Error (docker_centos): wrong response: ' + response)
            return -1
        return [creation, creation + execution]

    def podman(self):
        container, creation = podman.create("alpine-db-" + self.size + "-read", ["--rm"], [])
        response, execution = podman.start(container)
        if 'Done' not in response:
            print('Error (podman): wrong response: ' + response)
            return -1
        return [creation, creation + execution]

    def lxc(self):
        container, creation = lxc.init("alpine-db-" + self.size + "-read", ["-e"])
        start = lxc.start(container)
        response, execution_time = lxc.exec(container, ["./sqlite.sh", "tpcc.db", "read.sqlite"])
        if 'Done' not in response:
            print("Error (lxc): wrong response: " + response)
            return -1
        lxc.stop(container)
        return [creation, creation + start + execution_time]

    def runc(self):
        container, creation_time = runc.create("alpine-db-" + self.size + "-read")
        response, execution_time = runc.run(container, ["-o"])
        if 'Done' not in response:
            print("Error (runc): wrong response: " + response)
            return -1
        runc.clean(container)
        return [creation_time, creation_time + execution_time]

    def firecracker(self):
        return 0

    def kata(self):
        container, creation = kata.create("alpine-db-" + self.size + "-read", ["--rm"], [])
        response, execution = kata.start(container)
        if 'Done' not in response:
            print('Error (kata): wrong response: ' + response)
            return -1
        return [creation, creation + execution]
