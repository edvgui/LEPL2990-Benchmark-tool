#!/usr/bin/env python3
import subprocess
import sys


def usage():
    usage_msg = "Usage: contingious kill CONTAINER\n" \
                "\n" \
                "Kill a running CONTAINER\n\n"
    print(usage_msg)


def kill(name):
    """
    Kill a running container
    :param name: The name of the container
    :return: Return 0 if the container was successfully killed
    """
    command = "sh -c"
    args = command.split(" ")
    args.append("/usr/bin/crun kill %s 9; sleep 1; /usr/bin/crun delete %s" % (name, name))

    output = subprocess.run(args=args, stdout=sys.stdout, stderr=sys.stderr)
    if output.returncode != 0:
        print("Error: while trying to kill container", file=sys.stderr)
        return -1

    return 0


def main(argv):
    import getopt

    try:
        opts, args = getopt.getopt(argv[1:], "", [])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) != 1:
        print("Error: Exactly one argument is required, got %s" % len(args), file=sys.stderr)
        usage()
        return

    name = args[0]

    kill(name)


if __name__ == "__main__":
    main(sys.argv)
