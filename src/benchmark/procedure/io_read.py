from procedure.generic import Generic
import api.api_docker as docker
import api.api_podman as podman
import api.api_lxd as lxc
import api.api_contingious as contingious


class IORead(Generic):

    def __init__(self, size='xl'):
        super().__init__()
        if size not in ['xs', 'sm', 'md', 'lg', 'xl']:
            self.size = 'xl'
        else:
            self.size = size

    def name(self):
        return 'IO read ' + self.size

    def response_len(self):
        return 3

    def response_legend(self):
        return ["Create", "Start", "Exec"]

    def docker(self, image, runtime):
        options = ["--rm", "--network", "none"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        container, creation = docker.create("edvgui/%s-io-read-%s" % (image, self.size), options=options)
        _, start = docker.start(container)
        response, execution = docker.exec(container, ["/run/read", "/run/source"])
        docker.kill(container)
        if 'Done' not in response:
            print("Error (docker_alpine): wrong response: " + response)
            return -1
        return [creation, creation + start, creation + start + execution]

    def podman(self, image, runtime):
        options = ["--rm", "--network", "none"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        container, creation = podman.create("edvgui/%s-io-read-%s" % (image, self.size), options=options)
        _, start = podman.start(container)
        response, execution = podman.exec(container, ["/run/read", "/run/source"])
        podman.kill(container)
        if 'Done' not in response:
            print("Error (podman): wrong response: " + response)
            return -1
        return [creation, creation + start, creation + start + execution]

    def lxd(self, image, runtime):
        container, creation = lxc.init("edvgui/%s-io-read-%s" % (image, self.size), ["-e", "--profile", "default"])
        start = lxc.start(container)
        response, execution_time = lxc.exec(container, ["/root/read", "/root/%s" % self.size])
        lxc.kill(container)
        if 'Done' not in response:
            print("Error (lxc): wrong response: " + response)
            return -1
        return [creation, creation + start, creation + start + execution_time]

    def contingious(self, image, runtime):
        # TODO handle runtime
        container, creation_time = contingious.create("%s-db-%s-read" % (image, self.size))
        response, execution_time = contingious.run(container, ["-o"])
        contingious.clean(container)
        if 'Done' not in response:
            print("Error (runc): wrong response: " + response)
            return -1
        return [creation_time, creation_time + execution_time, creation_time + execution_time]

