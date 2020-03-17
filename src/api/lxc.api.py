import subprocess
import time


def init(image, log=False):
    """
    Initialize a container from an image with the command 'lxc init'
    :param image: The name of the image to create the container from
    :param log: Whether to display some logs or not
    :return: The id of the created container, the command execution time
    """
    args = ["lxc", "init", image]
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    return output.stdout.decode('utf-8').split(" ")[6].strip(), toc - tic


def start(container, log=False):
    """
    Start a previously created container with the command 'lxc start'
    :param container: The id of the created container
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    args = ["lxc", "start", container]
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
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
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    return output.stdout.decode('utf-8'), toc - tic


def stop(container, log=False):
    """
    Stop a running container with the command 'lxc stop'
    :param container: The id of the container to stop
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    args = ["lxc", "stop", container]
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
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
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    return toc - tic
