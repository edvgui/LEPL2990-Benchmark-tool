import subprocess
import time

from exceptions.api_exception import ApiException


class PodmanApiException(ApiException):

    def __init__(self, message, trace):
        super().__init__("Podman", message, trace)


def create(image, options, log=False):
    """
    Create a container with the command 'podman create'
    :param image: The name of the image to build the container from
    :param options: Options to pass to the command
    :param log: Whether logs should be displayed or not
    :return: The id of the created container, the command execution time
    """
    args = ["podman", "create", "-ti", "--cpus=1.0", "--memory=1g"]
    args.extend(options)
    args.append(image)
    args.append("sh")
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise PodmanApiException("Error while trying to create container from image " + image,
                                 output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def start(container, attach=False, log=False):
    """
    Start a container with the command 'podman start'
    :param container: The id of the previously created container to start
    :param attach: Whether to attach the execution or not
    :param log: Whether logs should be displayed or not
    :return: The output of the execution, the command execution time
    """
    args = ["podman", "start"]
    if attach:
        args.append("-a")
    args.append(container)
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise PodmanApiException("Error while trying to start container " + container,
                                 output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def exec(container, command, attach=True, log=False):
    """
    Execute a command in a running container
    :param container: The container in which execute the command
    :param command: The command to execute in the container
    :param attach: Whether to attach the execution or not
    :param log: Whether to display some logs or not
    :return: The output of the execution, the command execution time
    """
    args = ["podman", "exec"]
    if not attach:
        args.append("-d")
    args.append(container)
    args.extend(command)
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise PodmanApiException("Error while trying to execute command in container " + container,
                                 output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def run(image, options, command, log=False):
    """
    Run a command in a new container with the command 'podman run'
    :param image: The name of the image to build the container from
    :param options: The options to pass to 'podman run"
    :param command: The command to execute in the container
    :param log: Whether to display some logs or not
    :return: The output of the execution, the command execution time
    """
    args = ["podman", "run", "--cpus=1.0", "--memory=1g"]
    args.extend(options)
    args.append(image)
    args.extend(command)
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise PodmanApiException("Error while trying to run container from image " + image,
                                 output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def kill(container, log=False):
    """
    Stop a running container with the command 'podman stop'
    :param container: The id of the container to stop
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    args = ["podman", "kill", container]
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise PodmanApiException("Error while trying to stop container " + container,
                                 output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return toc - tic


def rm(container, log=False):
    """
    Remove a stopped container with the command 'podman rm'
    :param container: The id of the container to remove
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    args = ["podman", "rm", container]
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise PodmanApiException("Error while trying to remove container " + container,
                                 output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return toc - tic

