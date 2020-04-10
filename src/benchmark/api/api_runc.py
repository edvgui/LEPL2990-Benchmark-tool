import subprocess
import time
import os

from exceptions.api_exception import ApiException


class RuncApiException(ApiException):

    def __init__(self, message, trace):
        super().__init__("runc", message, trace)


directory = os.path.dirname(os.path.abspath(__file__))
runc_folder = os.path.join(directory, '../../../resources/runc')


def create(image, log=False):
    """
    Create all the component required to run a container with runc
    :param image: The custom image to take as basis
    :param log: Whether to display logs or not
    :return: The output of the command, the command execution time
    """
    path = os.path.join(runc_folder, 'create')
    args = [path, image]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise RuncApiException("Error while trying to create container from image " + image,
                               output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def run(container, options, log=False):
    """
    Run a previously created container with them command 'runc run'
    :param options: Options to be passed for the container run
    :param container: The name of the container to run
    :param log: Whether to display some logs or not
    :return: The execution output, the command execution time
    """
    path = os.path.join(runc_folder, 'run')
    args = [path]
    args.extend(options)
    args.append(container)
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise RuncApiException("Error while trying to run container " + container,
                               output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def stop(container, log=False):
    """
    Stop a running container
    :param container: The container to stop
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    path = os.path.join(runc_folder, 'stop')
    args = [path, container]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    if output.returncode != 0:
        raise RuncApiException("Error while trying to stop container " + container,
                               output.stderr.decode('utf-8').strip())
    return toc - tic


def clean(container, log=False):
    """
    Clean all the components created for a given container
    :param container: The container to clean
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    path = os.path.join(runc_folder, 'clean')
    args = [path, container]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.time()
    if output.returncode != 0:
        raise RuncApiException("Error while trying to clean container " + container,
                               output.stderr.decode('utf-8').strip())
    if log:
        print(output)
    return toc - tic
