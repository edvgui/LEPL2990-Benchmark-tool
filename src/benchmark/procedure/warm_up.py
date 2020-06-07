from procedure.generic import Generic
import api.api_docker as docker
import api.api_podman as podman
import api.api_lxd as lxc
import api.api_contingious as contingious


class WarmUp(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Warm up'

    def response_len(self):
        return 1

    def response_legend(self):
        return ["Run"]

    def docker(self, image, runtime):
        options = ["--rm"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        response, duration = docker.run("edvgui/%s-hello-world" % image, options=options, command=[])
        if 'Hello World' not in response:
            print('Error (docker_alpine): wrong response: ' + response)
        return [duration]

    def podman(self, image, runtime):
        options = ["--rm"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        response, duration = podman.run("edvgui/%s-hello-world" % image, options=options, command=[])
        if 'Hello World' not in response:
            print('Error (podman): wrong response: ' + response)
        return [duration]

    def lxd(self, image, runtime):
        container, launching_time = lxc.launch("edvgui/%s-hello-world" % image, ["-e"])
        response, execution_time = lxc.exec(container, ["/bin/echo", "Hello World"])
        if 'Hello World' not in response:
            print("Error (lxc): wrong response: " + response)
        lxc.kill(container)
        return [launching_time + execution_time]

    def contingious(self, image, runtime):
        container, creation = contingious.create("edvgui/%s-hello-world" % image)
        _, start = contingious.start(container)
        response, execution = contingious.exec(container, "/bin/echo Hello World")
        if "Hello World" not in response:
            print("Error (contingious): wrong response: " + response)
            return -1
        contingious.kill(container)
        contingious.clean(container)
        return [creation + start + execution]
