#!/usr/bin/env python3

import getopt
import os
import subprocess
import sys

from images import get_image, get_images


def usage():
    usage_msg = "Usage: python3 build.py [OPTIONS] IMAGE1 [IMAGE2 ..]\n" \
                "\n" \
                "Build the lxc images\n\n" \
                "Options:\n" \
                "  -h, --help               Display this message\n" \
                "  -d, --directory path     Base directory for the building scripts (default: ./)\n" \
                "  -a, --all                Build all the images\n" \
                "  -m, --match string       Images that contains the string" \
                "\n" \
                "Images:\n  %s" % "\n  ".join(get_images())

    print(usage_msg)


def build(name, directory):
    src, tag, build_args = get_image(name)

    command = [os.path.join(directory, src), tag]
    command.extend([v for v in build_args.values()])
    print("INFO: %s: Building" % tag)
    output = subprocess.run(args=command, stdout=subprocess.PIPE)
    if output.returncode != 0:
        print("Error building container %s" % name)
        return


def main(argv):
    directory = "/".join(argv[0].split("/")[0:-1])
    all_images = False
    match = []

    if len(argv) == 1:
        usage()
        sys.exit(0)

    try:
        opts, args = getopt.getopt(argv[1:], "hd:am:", ["help", "directory=", "all", "match="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-d", "--directory"):
            directory = arg
        elif opt == "--all":
            all_images = True
        elif opt in ("-m", "--match"):
            match.append(arg)

    if all_images:
        for i in get_images():
            build(i, directory)
        sys.exit(0)

    for m in match:
        for i in get_images():
            if m in i:
                build(i, directory)

    for a in args:
        if a not in get_images():
            print("Can not find %s in available images" % a)
        else:
            build(a, directory)


if __name__ == "__main__":
    main(sys.argv)
