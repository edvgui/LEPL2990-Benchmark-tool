import subprocess
import time


def create(image, log=False):
    pass


def run(path, log=False):
    """
    Run a previously created container with them command 'runc run'
    :param path: The path to the container to run
    :param log: Whether to display some logs or not
    :return: The execution output, the command execution time
    """
    args = ["runc", "run", "-b", path, path.split("/")[-1]]
    tic = time.time()
    output = subprocess.run(args=args, stdout=subprocess.PIPE)
    toc = time.time()
    if log:
        print(output)
    return output.stdout.decode('utf-8').strip(), toc - tic


def rm(path, log=False):
    pass
