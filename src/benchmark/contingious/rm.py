#!/usr/bin/env python3

import os
import random
import subprocess
import sys


def usage():
    usage_msg = "Usage: contingious rm [OPTIONS] CONTAINER\n" \
                "\n" \
                "Create a new container from the given IMAGE\n\n" \
                "Options:\n" \
                "      --network\n" \
                "      --pool-path string \n"
    print(usage_msg)


def rm(pool_path, name, network=False):
    """
    Remove a container a clean its namespace
    :param pool_path: The path to the pool where the container is stored
    :param name: The name of the container
    :param network: Whether the container has a network interface attached
    :return: True if the container was successfully removed
    """
    container_path = os.path.join(pool_path, name)
    if not os.path.exists(container_path):
        print("Error: This container could not be found in path %s" % container_path, file=sys.stderr)
        return False

    namespace_path = os.path.join(container_path, "namespace.pid")
    with open(namespace_path, 'r') as f:
        namespace_pid = f.readline().strip()
        f.close()

    if network:
        namespace_command = "/usr/bin/nsenter -t %s --user --mount --net sh -c" % namespace_pid
    else:
        namespace_command = "/usr/bin/nsenter -t %s --user --mount sh -c" % namespace_pid
    scope_command = "/usr/bin/systemd-run --user --scope --quiet %s" % namespace_command

    args = scope_command.split(" ")
    args.append("chown -R root:root %s" % container_path)

    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=sys.stderr)
    if output.returncode != 0:
        print("Error: while trying change ownership of container files", file=sys.stderr)
        return None

    command = "kill %s" % namespace_pid
    output = subprocess.run(args=command.split(" "), stdout=subprocess.PIPE)
    if output.returncode != 0:
        print("Error: While cleaning namespace", file=sys.stderr)
        return False

    command = "rm -rf %s" % container_path
    output = subprocess.run(args=command.split(" "), stdout=subprocess.PIPE)
    if output.returncode != 0:
        print("Error: While cleaning rootfs", file=sys.stderr)
        return False

    return True


def main(argv):
    import getopt

    try:
        opts, args = getopt.getopt(argv[1:], "", ["pool-path="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) != 1:
        print("Error: Exactly one argument is required, got %s" % len(args), file=sys.stderr)
        usage()
        return

    name = args[0]

    pool_path = os.path.join(os.path.expanduser("~"), '.local/share/contingious/storage/pool')
    network = False
    for opt, arg in opts:
        if opt == '--pool-path':
            pool_path = arg
        elif opt == '--network':
            network = True
        else:
            print("Error: Unknown option %s" % opt, file=sys.stderr)
            usage()
            return

    rm(pool_path, name, network)
    print(name)


if __name__ == "__main__":
    main(sys.argv)
