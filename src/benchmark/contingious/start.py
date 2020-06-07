#!/usr/bin/env python3
import array
import os
import socket
import subprocess
import sys


def usage():
    usage_msg = "Usage: contingious start CONTAINER\n" \
                "\n" \
                "Start a previously created container named CONTAINER\n\n" \
                "Options:" \
                "      --pool-path string\n"
    print(usage_msg)


def create_console_socket(console_socket):
    sock = socket.socket(socket.AF_UNIX)
    sock.bind(console_socket)
    sock.listen()
    return sock


def retrieve_console_fd(sock):
    fds = array.array('i')
    conn, _ = sock.accept()
    sock.close()
    msg, ancdata, msg_flags, _addr = conn.recvmsg(16, socket.CMSG_SPACE(fds.itemsize), socket.MSG_CMSG_CLOEXEC, )
    cmsg_level, cmsg_type, cmsg_data = ancdata[0]
    assert cmsg_level == socket.SOL_SOCKET, cmsg_level
    assert cmsg_type == socket.SCM_RIGHTS, cmsg_type
    fds.frombytes(cmsg_data)
    return list(fds)[0]


def start(pool_path, name, terminal, network=False):
    """
    Start a previously created container
    :param pool_path: The path of the pool where to container is stored
    :param name: The name of the container
    :param terminal: Whether to attach a terminal to the container
    :param network: Whether the container needs networking
    :return: 0 if everything is okay
    """
    container_path = os.path.join(pool_path, name)
    namespace_path = os.path.join(container_path, "namespace.pid")

    sock = None
    if terminal:
        console_socket = os.path.join(container_path, 'tty.sock')
        sock = create_console_socket(console_socket)
        create_command = "/usr/bin/crun --systemd-cgroup run --detach --bundle %s --console-socket %s %s" % (
            container_path, console_socket, name)
    else:
        create_command = "/usr/bin/crun --systemd-cgroup run --detach --bundle %s %s" % (container_path, name)

    with open(namespace_path, 'r') as f:
        namespace_pid = f.readline().strip()
        f.close()

    if network:
        namespace_command = "/usr/bin/nsenter -t %s --user --mount --net sh -c" % namespace_pid
    else:
        namespace_command = "/usr/bin/nsenter -t %s --user --mount sh -c" % namespace_pid
    scope_command = "/usr/bin/systemd-run --user --scope --quiet %s" % namespace_command

    args = scope_command.split(" ")
    args.append(create_command)

    output = subprocess.run(args=args, stdout=sys.stdout, stderr=sys.stderr)
    if output.returncode != 0:
        print("Error: while trying to start container", file=sys.stderr)
        return -1

    if terminal:
        # retrieve_console_fd(sock)
        pass

    return 0


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
    for opt, arg in opts:
        if opt == '--pool-path':
            pool_path = arg

    start(pool_path, name, True)
    print(name)


if __name__ == "__main__":
    main(sys.argv)
