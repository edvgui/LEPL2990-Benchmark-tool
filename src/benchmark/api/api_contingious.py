import time
import os

import contingious.create
import contingious.start
import contingious.exec
import contingious.kill
import contingious.rm
from exceptions.api_exception import ApiException


class ContingiousApiException(ApiException):

    def __init__(self, message, trace):
        super().__init__("Custom", message, trace)


images_path = os.path.join(os.path.expanduser("~"), '.local/share/contingious/storage/images')
pool_path = os.path.join(os.path.expanduser("~"), '/tmp/contingious-benchmark')


def create(image, network=False, port=None):
    """
    Create all the components required to run a container with runc
    :param image: The custom image to take as basis
    :param network: Whether to container needs a tap network interface
    :param port: The port to map in the network interface
    :return: The output of the command, the command execution time
    """
    image_path = os.path.join(images_path, image)
    tic = time.time()
    container = contingious.create.create(
        image_path,
        pool_path,
        contingious.create.generate_safe_id(pool_path),
        cmd="sleep infinity",
        network=network,
        port=port
    )
    toc = time.time()
    if container is None:
        raise ContingiousApiException("Error while creating container", "Unknown error")

    return container, toc - tic


def start(container, network=False):
    """
    Run a previously created container with them command 'runc run'
    :param container: The name of the container to run
    :param network: Whether the container has a network interface attached
    :return: The execution output, the command execution time
    """
    tic = time.time()
    result = contingious.start.start(pool_path, container, True, network=network)
    toc = time.time()
    if result != 0:
        raise ContingiousApiException("Error while starting container", "Unknown error")

    return result, toc - tic


def exec(container, command, network=False):
    """
    Execute a command in a running container
    :param container: The name of the container
    :param command: The command to execute in the container
    :param network: Whether the container has a network interface attached
    :return: The output of the command, the command execution time
    """
    tic = time.time()
    output = contingious.exec.exec(pool_path, container, command, network=network)
    toc = time.time()
    if output is None:
        raise ContingiousApiException("Error while executing command in container", "Unknown error")

    return output, toc - tic


def kill(container):
    """
    Stop a running container
    :param container: The container to stop
    :return: The command execution time
    """
    tic = time.time()
    result = contingious.kill.kill(container)
    toc = time.time()
    if result != 0:
        raise ContingiousApiException("Error while killing container", "Unknown error")

    return toc - tic


def clean(container, network=False):
    """
    Clean all the components created for a given container
    :param container: The container to clean
    :param network: Whether the container has a network interface attached
    :return: The command execution time
    """
    tic = time.time()
    result = contingious.rm.rm(pool_path, container, network=network)
    toc = time.time()
    if not result:
        raise ContingiousApiException("Error while killing container", "Unknown error")

    return toc - tic
