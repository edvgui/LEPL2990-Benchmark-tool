#!/usr/bin/env python3

import getopt
import subprocess
import sys

from images import get_image, get_images


def usage():
    usage_msg = "Usage: python3 build.py [OPTIONS] IMAGE1 [IMAGE2 ..]\n" \
                "\n" \
                "Pull docker images\n\n" \
                "Options:\n" \
                "  -h, --help               Display this message\n" \
                "  -a, --all                Pull all the images\n" \
                "  -m, --match string       Images that contains the string" \
                "\n" \
                "Images:\n  %s" % "\n  ".join(get_images())

    print(usage_msg)


def build(name):
    _, tag, _ = get_image(name)

    command = ["docker", "pull", tag]
    print("INFO: %s: Pulling" % tag)
    output = subprocess.run(args=command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode != 0:
        print("Error pulling container: %s" % output.stderr.decode('utf-8'))
        return


def main(argv):
    all_images = False
    match = []

    try:
        opts, args = getopt.getopt(argv[1:], "ham:", ["help", "all", "match="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "--all":
            all_images = True
        elif opt in ("-m", "--match"):
            match.append(arg)

    if all_images:
        for i in get_images():
            build(i)
        sys.exit(0)

    for m in match:
        for i in get_images():
            if m in i:
                build(i)

    for a in args:
        if a not in get_images():
            print("Can not find %s in available images" % a)
        else:
            build(a)


if __name__ == "__main__":
    main(sys.argv)
