#!/usr/bin/env python3
import array
import json
import os
import random
import socket
import subprocess
import sys
import time

if __name__ == '__main__':
    from container_config import generate_config
else:
    from contingious.container_config import generate_config


def usage():
    usage_msg = "Usage: contingious create [OPTIONS] IMAGE [COMMAND]\n" \
                "\n" \
                "Create a new container from the given IMAGE\n\n" \
                "Options:\n" \
                "  -n, --name string\n" \
                "      --network \n" \
                "  -p, --port string\n" \
                "      --terminal \n" \
                "      --images-path string  \n" \
                "      --pool-path string \n"
    print(usage_msg)


def generate_safe_id(pool_path):
    hash_b = random.getrandbits(256)
    _id = "%032x" % hash_b
    while os.path.isdir(os.path.join(pool_path, _id)):
        hash_b = random.getrandbits(256)
        _id = "%032x" % hash_b
    return _id


def create(image_path, pool_path, name, cmd, network=False, port=None, terminal=False):
    """
    Create a container from image_path and store it at pool_path
    :param image_path: The path to the image
    :param pool_path: The pool where to store the container
    :param name: The name to give to the container
    :param cmd: The command that container should execute on start
    :param network: Whether to attach a network tap interface
    :param port: Ports to map
    :param terminal: Whether to attach a terminal
    :return: The name of the created container, or None is an error occurred
    """
    if not os.path.exists(image_path):
        print("Error: This image could not be found in path %s" % image_path, file=sys.stderr)
        return None

    container_path = os.path.join(pool_path, name)
    if os.path.exists(container_path):
        print("Error: A container is existing at that path: %s" % container_path, file=sys.stderr)
        return None

    os.makedirs(container_path)
    rootfs = os.path.join(image_path, 'rootfs')
    command = "cp -r %s %s" % (rootfs, container_path)
    output = subprocess.run(args=command.split(" "), stdout=subprocess.PIPE)
    if output.returncode != 0:
        print("Error: While copying rootfs", file=sys.stderr)
        return None

    if cmd is None:
        cmd_path = os.path.join(image_path, 'CMD')
        with open(cmd_path, 'r') as f:
            cmd = f.readline()
            f.close()

    config = generate_config(name, container_path, image_path, cmd.split(" "), network, terminal)
    config_path = os.path.join(container_path, 'config.json')
    with open(config_path, 'w+') as f:
        json.dump(config, f, indent=4)

    command = "/usr/bin/rootlesskit"
    if network:
        command += " --net=slirp4netns --disable-host-loopback --copy-up=/etc"
    if port is not None:
        command += " --port-driver=builtin --publish %s" % port
    command += " /bin/sh -c"

    namespace_path = os.path.join(container_path, 'namespace.pid')

    args = command.split(" ")
    args.append("echo $$ > %s; sleep infinity" % namespace_path)
    output = subprocess.Popen(args=args, stdout=None, stderr=None, stdin=None)

    while not os.path.exists(namespace_path):
        time.sleep(0.001)

    return name


def main(argv):
    import getopt

    try:
        opts, args = getopt.getopt(argv[1:], "n:p:",
                                   ["name=", "network", "port=", "terminal", "images-path=", "pool-path="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) < 1:
        print("Error: At least one argument is required, got %s" % len(args), file=sys.stderr)
        usage()
        return

    image = args[0]

    cmd = None
    if len(args) > 1:
        cmd = " ".join(args[1:])

    name = None
    network = False
    port = None
    terminal = False
    images_path = os.path.join(os.path.expanduser("~"), '.local/share/contingious/storage/images')
    pool_path = os.path.join(os.path.expanduser("~"), '.local/share/contingious/storage/pool')
    for opt, arg in opts:
        if opt in ('-n', '--name'):
            name = arg
        elif opt == '--network':
            network = True
        elif opt in ('-p', '--port'):
            port = arg
        elif opt == '--terminal':
            terminal = True
        elif opt == '--images-path':
            images_path = arg
        elif opt == '--pool-path':
            pool_path = arg
        else:
            print("Error: Unknown option %s" % opt, file=sys.stderr)
            usage()
            return

    if name is None:
        name = generate_safe_id(pool_path)

    print(create(os.path.join(images_path, image), pool_path, name, cmd, network=network, port=port, terminal=terminal))


if __name__ == "__main__":
    main(sys.argv)
