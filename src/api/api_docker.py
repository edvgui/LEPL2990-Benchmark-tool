import subprocess
import time


def create(image, options, log=False):
    """
    Create a container with the command 'docker create'
    :param image: The name of the image to build the container from
    :param options: Options to pass to the command
    :param log: Whether logs should be displayed or not
    :return: The id of the created container, the command execution time
    """
    args = ["docker", "create"]
    args.extend(options)
    args.append(image)
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def start(container, attach=True, log=False):
    """
    Start a container with the command 'docker start'
    :param container: The id of the previously created container to start
    :param attach: Whether to attach the execution or not
    :param log: Whether logs should be displayed or not
    :return: The output of the execution, the command execution time
    """
    args = ["docker", "start"]
    if attach:
        args.append("-a")
    args.append(container)
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def run(image, options, command, log=False):
    """
    Run a command in a new container with the command 'docker run'
    :param image: The name of the image to build the container from
    :param options: The options to pass to 'docker run"
    :param command: The command to execute in the container
    :param log: Whether to display some logs or not
    :return: The output of the execution, the command execution time
    """
    args = ["docker", "run"]
    args.extend(options)
    args.append(image)
    args.extend(command)
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def stop(container, log=False):
    """
    Stop a running container with the command 'docker stop'
    :param container: The id of the container to stop
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    args = ["docker", "stop", container]
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    return toc - tic


def rm(container, log=False):
    """
    Remove a stopped container with the command 'docker rm'
    :param container: The id of the container to remove
    :param log: Whether to display some logs or not
    :return: The command execution time
    """
    args = ["docker", "rm", container]
    tic = time.time()
    output = subprocess.run(args, stdout=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    return toc - tic
