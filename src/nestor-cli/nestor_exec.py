#!/usr/bin/env python3
import getopt
import json
import os
import socket
import sys

from nestor_config import load as get_config


def usage():
    usage_msg = "Usage: nestor exec [OPTIONS] CONTAINER COMMAND ARGS...\n" \
                "\n" \
                "Execute a COMMAND in a running CONTAINER\n\n" \
                "Options:" \
                "  -d, --detach\n" \
                "  -t, --tty\n"
    print(usage_msg)


def main(argv):
    config = get_config()
    try:
        socket_container_daemon = config["container-daemon"]["socket"]
    except KeyError:
        print("ERROR: Bad configuration file")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv[1:], "dt", ["detach", "tty"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) < 2:
        usage()
        exit(1)

    container = args[0]
    cmd = args[1:] if len(args) > 1 else None

    detach = False
    terminal = False
    for opt, arg in opts:
        if opt in ('-d', '--detach'):
            detach = True
        elif opt in ('-t', '--tty'):
            terminal = True

    container_socket_path = os.path.join(socket_container_daemon, container + ".sock")

    sock = socket.socket(socket.AF_UNIX)
    sock.connect(container_socket_path)
    fd = sock.fileno()
    w = open(fd, 'w')
    w.write(json.dumps({
        "command": "exec",
        "args": {
            "detach": detach,
            "terminal": terminal,
            "cmd": cmd
        }
    }))
    w.write('\n')
    w.flush()

    r = open(fd, 'r')
    response_string = r.readline()
    response = json.loads(response_string)
    sock.close()
    if response["status"] == "success":
        print(response["value"])
    else:
        print(response["message"], file=sys.stderr)


if __name__ == "__main__":
    os.environ["CONFIG"] = os.path.join(os.path.expanduser("~"), '.config/nestor/config.json')
    main(sys.argv)
