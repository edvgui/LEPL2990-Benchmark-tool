#!/usr/bin/env python3
import os
import sys
import getopt


def usage():
    usage_msg = "Usage: nestor [OPTIONS] COMMAND \n" \
        "\n" \
        "Manage and run basic and rootless containers with nestor\n\n" \
        "Options:\n" \
        "  -D, --debug           Display debug information\n" \
        "  -C, --config string   Path to the configuration file to use\n" \
        "\n" \
        "Commands:\n" \
        "  help        Display this message\n" \
        "  create      Create a new container\n" \
        "  config      Display current configuration\n" \
        "  exec        Execute a command in a running container\n" \
        "  images      List available images\n" \
        "  kill        Kill one or more running containers\n" \
        "  pull        Build a new container image from its docker equivalent\n" \
        "  ps          List containers\n" \
        "  start       Start a stopped container\n" \
        "  rm          Remove a stopped container\n" \
        "  rmi         Remove container images\n" \
        "  run         Create and start a new container\n"
    print(usage_msg)


def call_command(args):
    command = args[0]
    if command == "pull":
        from nestor_pull import main as pull
        pull(args)
    elif command == "config":
        from nestor_config import main as config
        config(args)
    elif command == "create":
        from nestor_create import main as create
        create(args)
    elif command == "exec":
        from nestor_exec import main as exec
        exec(args)
    elif command == "images":
        from nestor_images import main as images
        images(args)
    elif command == "kill":
        from nestor_kill import main as kill
        kill(args)
    elif command == "ps":
        from nestor_ps import main as ps
        ps(args)
    elif command == "start":
        from nestor_start import main as start
        start(args)
    elif command == "status":
        from nestor_status import main as status
        status(args)
    elif command == "rm":
        from nestor_rm import main as rm
        rm(args)
    elif command == "rmi":
        from nestor_rmi import main as rmi
        rmi(args)
    elif command == "run":
        from nestor_run import main as run
        run(args)
    elif command == "help":
        usage()
    else:
        usage()
        sys.exit(1)


def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "DC:", ["debug", "config="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    os.environ["CONFIG"] = os.path.join(os.path.expanduser("~"), '.config/nestor/config.json')
    for opt, arg in opts:
        if opt in ('-C', '--config'):
            os.environ["CONFIG"] = arg
        elif opt in ('-D', '--debug'):
            pass

    if len(args) == 0:
        usage()
        exit(1)

    call_command(args)


if __name__ == "__main__":
    main(sys.argv)
