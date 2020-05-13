from procedure.generic import Generic
import api.api_docker as docker
import api.api_podman as podman
import api.api_lxc as lxc
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
        if 'Hello World' not in response:
            print('Error (docker_alpine): wrong response: ' + response)
        docker.kill(container)
        return [creation, creation + start, creation + start + execution]

    def podman(self, image, runtime):
        options = ["--rm", "--network", "none"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        container, creation = podman.create("edvgui/%s-hello-world" % image, options=options)
        _, start = podman.start(container)
        response, execution = podman.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print('Error (podman_alpine): wrong response: ' + response)
        podman.kill(container)
        return [creation, creation + start, creation + start + execution]

    def lxc(self, image, runtime):
        container, creation = lxc.init("%s-hello-world" % image, ["-e", "--profile", "default"])
        start = lxc.start(container)
        response, execution_time = lxc.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print("Error (lxc): wrong response: " + response)
        lxc.stop(container)
        return [creation, creation + start, creation + start + execution_time]

    def contingious(self, image, runtime):
        # TODO handle runtime
        container, creation_time = contingious.create("%s-hello-world" % image)
        response, execution_time = contingious.run(container, ["-o"])
        if 'Hello World' not in response:
            print("Error (runc): wrong response: " + response)
        contingious.clean(container)
        return [creation_time, creation_time + execution_time, creation_time + execution_time]
