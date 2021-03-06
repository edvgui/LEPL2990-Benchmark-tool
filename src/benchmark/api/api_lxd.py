import subprocess
import time

from exceptions.api_exception import ApiException


class LXCApiException(ApiException):

    def __init__(self, message, trace):
        super().__init__("LXD", message, trace)


def init(image, flags, log=False):
    """
    Initialize a container from an image with the command 'lxc init'
    :param image: The name of the image to create the container from
    :param flags: Some flags to pass for the creation
    :param log: Whether to display some logs or not
    :return: The id of the created container, the command execution time
    """
    args = ["lxc", "init", image]
    args.extend(flags)
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise LXCApiException("Error while trying to initiate container from image " + image,
                              output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.stdout.decode('utf-8').split(" ")[5].strip(), toc - tic


def start(container, log=False):
    """
    Start a previously created container with the command 'lxc start'
    :param container: The id of the created container
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    args = ["lxc", "start", container]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise LXCApiException("Error while trying to start container " + container,
                              output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return toc - tic


def exec(container, command, log=False):
    """
    Execute a command in a running container with the command 'lxc exec'
    :param container: The id of the container in which execute the command
    :param command: The command to execute
    :param log: Whether to display some logs or not
    :return: The output of the execution, the command execution time
    """
    args = ["lxc", "exec", container, "--"]
    args.extend(command)
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise LXCApiException("Error while trying to execute command '{0}' in container {1}".format(command, container),
                              output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.stdout.decode('utf-8'), toc - tic


def launch(image, options, log=False):
    """
    Build and start a new container with the command 'lxc launch'
    :param image: The image to build the container from
    :param options: The options to give for the launch
    :param log: Whether to display some logs or not
    :return: The id of the launched container, the command execution time
    """
    args = ["lxc", "launch", image]
    args.extend(options)
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise LXCApiException("Error while trying to launch container from image " + image,
                              output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.stdout.decode('utf-8').split(" ")[6].strip(), toc - tic


def kill(container, log=False):
    """
    Stop a running container with the command 'lxc stop'
    :param container: The id of the container to stop
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    args = ["lxc", "stop", "--force", container]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise LXCApiException("Error while trying to stop container " + container,
                              output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return toc - tic


def rm(container, log=False):
    """
    Remove a stopped container with the command 'lxc rm'
    :param container: The id of the container to remove
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    args = ["lxc", "rm", container]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise LXCApiException("Error while trying to remove container " + container,
                              output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return toc - tic
