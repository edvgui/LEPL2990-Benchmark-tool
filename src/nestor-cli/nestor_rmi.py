#!/usr/bin/env python3
import getopt
import os
import shutil
import sys

from nestor_config import load as get_config


def usage():
    usage_msg = "Usage: nestor rmi IMAGE [IMAGE2...]\n" \
          "\n" \
          "Delete container images\n\n"
    print(usage_msg)


def main(argv):
    config = get_config()
    try:
        images_storage = config["storage"]["images"]
    except KeyError:
        print("ERROR: Bad configuration file, missing storage.images")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv[1:], "", [""])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) == 0:
        usage()
        exit(1)

    for image in args:
        folder = os.path.join(images_storage, image)
        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder)
            except shutil.Error as e:
                print("ERROR: %s" % e.strerror)
        else:
            print("ERROR: This image doesn't exists: %s" % image)
