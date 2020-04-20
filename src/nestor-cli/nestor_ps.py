#!/usr/bin/env python3
import getopt
import os
import subprocess
import sys

from nestor_config import load as get_config


def usage():
    usage_msg = "Usage: nestor ps [OPTION]\n" \
                "\n" \
                "Display the list of existing containers with their state\n\n" \
                "Option:" \
                "      --runtime string"
    print(usage_msg)


def main(argv):
    config = get_config()
    try:
        r = config["default-runtime"]
        available_runtimes = config["runtimes"]
        runtime = available_runtimes[r]
    except KeyError:
        print("ERROR: Bad configuration file")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv[1:], "", ["runtime="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) != 0:
        usage()
        exit(1)

    for opt, arg in opts:
        if opt == '--runtime':
            if arg in available_runtimes:
                runtime = available_runtimes[arg]
            else:
                print("ERROR: This runtime isn't available: %s" % arg)
                sys.exit(1)

    args = [runtime["path"], "--root", runtime["root"], "list"]
    output = subprocess.run(args, stdout=sys.stdout, stderr=sys.stderr)
    if output.returncode != 0:
        print("ERROR: Couldn't list containers: %s" % output.stderr.decode('utf-8'))
        sys.exit(1)


if __name__ == "__main__":
    os.environ["CONFIG"] = os.path.join(os.path.expanduser("~"), '.config/nestor/config.json')
    main(sys.argv)
