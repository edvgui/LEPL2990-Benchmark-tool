#!/usr/bin/env python3
import os
import subprocess
import sys


def usage():
    usage_msg = "Usage: contingious exec [OPTIONS] CONTAINER COMMAND\n" \
                "\n" \
                "Execute a COMMAND in a running CONTAINER\n\n" \
                "Options:\n" \
                "      --network \n" \
                "      --pool-path string \n"
    print(usage_msg)


def exec(pool_path, name, command, network=False):
    """
    Execute a command in a running container
    :param pool_path: The path to the pool where the container is stored
    :param name: The name of the container
    :param command: The command to run in the container
    :param network: Whether the container has a network interface attached to it
    :return: The output of the command
    """
    container_path = os.path.join(pool_path, name)
    namespace_path = os.path.join(container_path, "namespace.pid")
    with open(namespace_path, 'r') as f:
        namespace_pid = f.readline().strip()
        f.close()

    exec_command = "/usr/bin/crun exec %s %s;" % (name, command)
    if network:
        namespace_command = "/usr/bin/nsenter -t %s --user --mount --net sh -c" % namespace_pid
    else:
        namespace_command = "/usr/bin/nsenter -t %s --user --mount sh -c" % namespace_pid
    scope_command = "/usr/bin/systemd-run --user --scope --quiet %s" % namespace_command

    args = scope_command.split(" ")
    args.append(exec_command)

    output = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=sys.stderr)
    if output.returncode != 0:
        print("Error: while trying to exec command in container", file=sys.stderr)
        return None

    return output.stdout.decode('utf-8')


def main(argv):
    import getopt

    try:
        opts, args = getopt.getopt(argv[1:], "", ["pool-path="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) < 2:
        print("Error: One container and one command needs to be provided, got %s arguments" % len(args), file=sys.stderr)
        usage()
        return

    name = args[0]
    command = " ".join(args[1:])

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

    print(exec(pool_path, name, command, network))


if __name__ == "__main__":
    main(sys.argv)
