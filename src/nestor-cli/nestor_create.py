#!/usr/bin/env python3
import getopt
import json
import os
import socket
import sys
from multiprocessing import Process, Queue

import nestor_container
from nestor_config import load as get_config


def usage():
    usage_msg = "Usage: nestor create [OPTIONS] IMAGE [COMMAND]\n" \
        "\n" \
        "Create a new container from the given IMAGE\n\n" \
        "Options:\n" \
        "      --name string\n" \
        "  -n, --network\n" \
        "  -p, --port address:port:port\n" \
        "      --rm\n" \
        "      --runtime string\n" \
        "  -t, --tty\n"
    print(usage_msg)


def main(argv):
    config = get_config()
    try:
        images_storage = config["storage"]["images"]
        pool_storage = config["storage"]["pool"]
        socket_container_daemon = config["container-daemon"]["socket"]
        pid_container_daemon = config["container-daemon"]["pid"]
        r = config["default-runtime"]
        available_runtimes = config["runtimes"]
        runtime = available_runtimes[r]
    except KeyError:
        print("ERROR: Bad configuration file")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv[1:], "inp:t", ["interactive", "name=", "network", "port=", "rm", "runtime=",
                                                       "tty"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) == 0:
        usage()
        exit(1)
    image = args[0]
    image_dir = os.path.join(images_storage, image)
    if not os.path.isdir(image_dir):
        print("ERROR: This image doesn't exist")
        sys.exit(1)

    cmd = args[1:] if len(args) > 1 else None

    name = None
    network = False
    port = None
    rm = False
    terminal = False
    for opt, arg in opts:
        if opt == '--name':
            name = arg
        elif opt in ('-n', '--network'):
            network = True
        elif opt in ('-p', '--port'):
            port = arg
            network = True
        elif opt == '--rm':
            rm = True
        elif opt == '--runtime':
            if arg in available_runtimes:
                runtime = available_runtimes[arg]
            else:
                print("ERROR: This runtime isn't available: %s" % arg)
                sys.exit(1)
        elif opt in ('-t', '--tty'):
            terminal = True

    queue = Queue()
    p = Process(target=nestor_container.main, args=(
        ["nestor_container", "--socket-dir", socket_container_daemon, "--pid-dir", pid_container_daemon, pool_storage],
        queue,
    ))
    p.start()
    p.join()
    container_socket_path = queue.get()

    sock = socket.socket(socket.AF_UNIX)
    sock.connect(container_socket_path)
    fd = sock.fileno()
    w = open(fd, 'w')
    w.write(json.dumps({
        "command": "create",
        "args": {
            "image": image_dir,
            "name": name,
            "network": network,
            "port": port,
            "auto_remove": rm,
            "terminal": terminal,
            "runtime": runtime,
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
