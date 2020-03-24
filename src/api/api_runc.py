import subprocess
import time
import os

from src.exceptions.api_exceptions import ApiException


class RuncApiException(ApiException):

    def __init__(self, message, trace):
        super().__init__("runc", message, trace)


directory = os.path.dirname(os.path.abspath(__file__))
runc_folder = os.path.join(directory, '../../resources/runc')
commands = os.path.join(runc_folder, 'commands')
pool = os.path.join(runc_folder, 'pool')


def create(image, log=False):
    """
    Create all the component required to run a container with runc
    :param image: The custom image to take as basis
    :param log: Whether to display logs or not
    :return: The return code of the creation script, the output of the command, the command execution time
    """
    path = os.path.join(commands, 'create')
    args = [path, image]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise RuncApiException("Error while trying to create container from image " + image,
                               output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.returncode, output.stdout.decode('utf-8').strip(), toc - tic


def run(container, log=False):
    """
    Run a previously created container with them command 'runc run'
    :param container: The name of the container to run
    :param log: Whether to display some logs or not
    :return: The return code of the command, the execution output, the command execution time
    """
    path = os.path.join(pool, container)
    args = ["runc", "run", "-b", path, container]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise RuncApiException("Error while trying to run container " + container,
                               output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.returncode, output.stdout.decode('utf-8').strip(), toc - tic


def clean(container, log=False):
    """
    Clean all the components created for a given container
    :param container: The container to clean
    :param log: Whether to display some logs or not
    :return: The return code of the command, the execution output, the command execution time
    """
    path = os.path.join(commands, 'clean')
    args = [path, container]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise RuncApiException("Error while trying to clean container " + container,
                               output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.returncode, output.stdout.decode('utf-8').strip(), toc - tic
