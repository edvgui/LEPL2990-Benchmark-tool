#!/usr/bin/env python3
import os
import json


def load():
    path = os.environ["CONFIG"]
    try:
        with open(path, 'r') as f:
            config = json.load(f)
            f.close()
    except FileNotFoundError:
        print("ERROR: Configuration file not found at path: " + path)
        config = {}
    return config


def usage():
    usage_msg = "Usage: nestor config\n" \
          "\n" \
          "Display the current configuration\n\n"
    print(usage_msg)


def print_object(path, obj):
    for i in obj:
        n_path = path + "." + i
        if type(obj[i]) is dict:
            print_object(n_path, obj[i])
        else:
            print("  " + n_path + "=" + obj[i])


def main(argv):
    config = load()
    print("Configuration file: %s" % os.environ["CONFIG"])
    print_object("config", config)
