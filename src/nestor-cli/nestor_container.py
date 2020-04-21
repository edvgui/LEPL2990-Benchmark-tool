#!/usr/bin/env python3
import json
import os
import sys
import socket
import getopt
from json import JSONDecodeError
from multiprocessing import Queue

from container import Container, ContainerException


def loop(sock, container, callback):
    done = False
    while not done:
        conn, _ = sock.accept()
        fd = conn.fileno()
        incoming = open(fd, 'r')
        request_string = incoming.readline()
        try:
            request = json.loads(request_string)
            response = {
                "status": "success",
                "value": None
            }

            command = request["command"]
            args = request["args"]
            if command == 'create':
                response["value"] = container.create(
                    image=args["image"],
                    runtime=args["runtime"],
                    name=args["name"],
                    network=args["network"],
                    port=args["port"],
                    auto_remove=args["auto_remove"],
                    terminal=args["terminal"],
                    cmd=args["cmd"]
                )
            elif command == 'exec':
                response["value"] = container.exec(
                    cmd=args["cmd"],
                    detach=args["detach"],
                    terminal=args["terminal"]
                )
            elif command == 'kill':
                response["value"] = container.kill()
            elif command == 'rm':
                response["value"] = container.rm()
                done = True
            elif command == 'run':
                response["value"] = container.run(
                    image=args["image"],
                    runtime=args["runtime"],
                    name=args["name"],
                    detach=args["detach"],
                    network=args["network"],
                    port=args["port"],
                    auto_remove=args["auto_remove"],
                    terminal=args["terminal"],
                    cmd=args["cmd"]
                )
            elif command == 'start':
                response["value"] = container.start(
                    attach=args["attach"]
                )
            elif command == 'state':
                response["value"] = {
                    "image": container.image,
                    "name": container.name,
                    "network": container.network,
                    "port": container.port,
                    "auto_remove": container.auto_remove,
                    "tty": container.tty,
                    "runtime": container.runtime,
                    "cmd": container.cmd,
                    "state": str(container.state)
                }
        except JSONDecodeError:
            response = {
                "status": "error",
                "error": "Bad request",
                "message": "Bad json input: %s" % request_string
            }
        except KeyError as e:
            response = {
                "status": "error",
                "error": "Bad request",
                "message": e.args
            }
        except ContainerException as e:
            response = {
                "status": "error",
                "error": "Container daemon error",
                "message": str(e)
            }
        except Exception as e:
            response = {
                "status": "error",
                "error": "Unknown error",
                "message": str(e)
            }

        outgoing = open(fd, 'w')
        outgoing.write(json.dumps(response))
        outgoing.write("\n")
        outgoing.flush()
        outgoing.close()
        del incoming
        del outgoing
        del conn

    callback()


def daemonize(pid_path):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("First fork failed %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("Second fork failed %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open(os.devnull, 'a+')
    se = open(os.devnull, 'a+')

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stdout.fileno())

    pid = str(os.getpid())
    with open(pid_path, 'w+') as f:
        f.write(pid + '\n')
        f.close()


def usage():
    usage_msg = "Usage: nestor_container [OPTIONS] POOL\n" \
                "\n" \
                "Create a process managing a container commendable through POSIX socket.\n" \
                "The POOL in which the container will be located should be provided\n" \
                "Print to stdout the path to the socket to communicate with the process.\n\n" \
                "Options:\n" \
                "      --socket-dir string   Directory where to create the socket (default \n" \
                "                            /run/user/1000/nestor/socket/)\n" \
                "      --pid-dir string      Directory where to save the pid (default /run/\n" \
                "                            user/1000/nestor/pid/)\n"
    print(usage_msg)


def main(argv, q):
    socket_dir = '/run/user/1000/nestor/socket'
    pid_dir = '/run/user/1000/nestor/pid'

    try:
        opts, args = getopt.getopt(argv[1:], "", ["socket-dir=", "pid-dir="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    if len(args) != 1:
        print("ERROR: One argument is required", file=sys.stderr)
        usage()
        sys.exit(1)

    pool = args[0]

    for opt, arg in opts:
        if opt == "--socket-dir":
            socket_dir = arg
        elif opt == "--pid-dir":
            pid_dir = arg

    if not os.path.isdir(socket_dir):
        os.makedirs(socket_dir, exist_ok=True)

    if not os.path.isdir(pid_dir):
        os.makedirs(pid_dir, exist_ok=True)

    container = Container(socket_dir, pool)
    socket_path = os.path.join(socket_dir, container.get_id() + '.sock')
    pid_path = os.path.join(pid_dir, container.get_id() + '.pid')
    sock = socket.socket(socket.AF_UNIX)
    sock.bind(socket_path)
    sock.listen()

    def callback():
        os.remove(pid_path)
        sock.close()
        os.remove(socket_path)

    q.put(socket_path)
    daemonize(pid_path)
    loop(sock, container, callback)


if __name__ == "__main__":
    main(sys.argv, Queue())