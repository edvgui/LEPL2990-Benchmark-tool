from procedure.generic import Generic
import api.api_docker as docker
import api.api_podman as podman
import api.api_lxd as lxc
import api.api_contingious as contingious
import time


class Ping(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Ping'

    def response_len(self):
        return 1

    def response_legend(self):
        return ["Ping"]

    def docker(self, image, runtime):
        options = ["--rm"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        try:
            response, _ = docker.run("edvgui/%s-ping" % image, options=options, command=[])
        except docker.DockerApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (docker_alpine): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]

    def podman(self, image, runtime):
        options = ["--rm"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        try:
            response, _ = podman.run("edvgui/%s-ping" % image, options=options, command=[])
        except podman.PodmanApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (podman): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]

    def lxd(self, image, runtime):
        container, launching_time = lxc.launch("edvgui/%s-ping" % image, ["-e", "--profile", "default", "--profile",
                                                                      "online"])
        for i in range(0, 10):
            try:
                response, _ = lxc.exec(container, ["./ping.sh", "10"])
            except lxc.LXCApiException:
                pass
            else:
                lxc.kill(container)
                if '=' not in response:
                    print('Error (lxc): wrong response: ' + response)
                    return -1
                else:
                    return [float(response.split(" ")[3].split("/")[1]) / 1000]
            time.sleep(1)
        lxc.kill(container)
        print('Error (lxc): maximum retry reached')
        return -1

    def contingious(self, image, runtime):
        container, creation = contingious.create("edvgui/%s-ping" % image, network=True)
        _, start = contingious.start(container, network=True)
        try:
            response, execution = contingious.exec(container, "/run/run.sh", network=True)
        except contingious.ContingiousApiException as e:
            print(e)
            contingious.kill(container)
            contingious.clean(container)
            return -1
        else:
            contingious.kill(container)
            contingious.clean(container)
            if '=' not in response:
                print('Error (contingious): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]
