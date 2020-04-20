#!/usr/bin/env python3
import os
import sys

from nestor_config import load as get_config


def usage():
    usage_msg = "Usage: nestor images\n" \
          "\n" \
          "List available images\n\n"
    print(usage_msg)


def list_images():
    config = get_config()
    try:
        images_storage = config["storage"]["images"]
    except KeyError:
        print("ERROR: Bad configuration file, missing storage.images")
        sys.exit(1)

    for f in os.listdir(images_storage):
        if os.path.isdir(os.path.join(images_storage, f)):
            yield f


def main(argv):
    for image in list_images():
        print(image)
