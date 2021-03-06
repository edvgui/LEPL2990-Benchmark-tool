from procedure.generic import Generic
import api.api_docker as docker
import api.api_podman as podman
import api.api_lxd as lxc
import api.api_contingious as contingious


class HelloWorld(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Hello World'

    def response_len(self):
        return 3

    def response_legend(self):
        return ["Create", "Start", "Exec"]

    def docker(self, image, runtime):
        options = ["--rm", "--network", "none"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        container, creation = docker.create("edvgui/%s-hello-world" % image, options=options)
        _, start = docker.start(container)
        response, execution = docker.exec(container, ["/bin/echo", "Hello World"])
        docker.kill(container)
        if 'Hello World' not in response:
            print('Error (docker): wrong response: ' + response)
            return -1
        return [creation, creation + start, creation + start + execution]

    def podman(self, image, runtime):
        options = ["--network", "none"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        container, creation = podman.create("edvgui/%s-hello-world" % image, options=options)
        _, start = podman.start(container)
        response, execution = podman.exec(container, ["/bin/echo", "Hello World"])
        podman.kill(container)
        podman.rm(container)
        if 'Hello World' not in response:
            print('Error (podman): wrong response: ' + response)
            return -1
        return [creation, creation + start, creation + start + execution]

    def lxd(self, image, runtime):
        container, creation = lxc.init("edvgui/%s-hello-world" % image, ["-e", "--profile", "default"])
        start = lxc.start(container)
        response, execution_time = lxc.exec(container, ["/bin/echo", "Hello World"])
        lxc.kill(container)
        if 'Hello World' not in response:
            print("Error (lxc): wrong response: " + response)
            return -1
        return [creation, creation + start, creation + start + execution_time]

    def contingious(self, image, runtime):
        container, creation = contingious.create("edvgui/%s-hello-world" % image)
        _, start = contingious.start(container)
        response, execution = contingious.exec(container, "/bin/echo Hello World")
        if "Hello World" not in response:
            print("Error (contingious): wrong response: " + response)
            return -1
        contingious.kill(container)
        contingious.clean(container)
        return [creation, creation + start, creation + start + execution]
