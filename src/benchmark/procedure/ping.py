from procedure.generic import Generic
import api.api_docker as docker
import api.api_podman as podman
import api.api_lxc as lxc
import api.api_custom as custom
import time


class Ping(Generic):

    def __init__(self):
        super().__init__()

    def name(self):
        return 'Network'

    def response_len(self):
        return 1

    def response_legend(self):
        return ["Ping"]

    def docker(self, image, runtime):
        options = ["--rm"]
        if runtime is not None:
            options.extend(["--runtime", runtime])
        try:
            response, _ = docker.run("edvgui/%s-network" % image, options=options, command=[])
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
            response, _ = podman.run("edvgui/%s-network" % image, options=options, command=[])
        except podman.PodmanApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (podman): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]

    def lxc(self, image, runtime):
        container, launching_time = lxc.launch("%s-network" % image, ["-e"])
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

    def custom(self, image, runtime):
        # TODO handle runtime
        container, _ = custom.create("%s-network" % image)
        try:
            response, _ = custom.run(container, [])
        except custom.CustomApiException as e:
            print(e)
            return -1
        else:
            if '=' not in response:
                print('Error (custom): wrong response: ' + response)
                return -1
            else:
                return [float(response.split(" ")[3].split("/")[1]) / 1000]
        finally:
            custom.clean(container)
