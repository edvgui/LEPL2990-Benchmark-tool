#!/usr/bin/env python3

import getopt
import os
import subprocess
import sys


images = {
    "alpine-hello-world": {
        "path": "alpine-hello-world/Dockerfile",
        "tag": "edvgui/alpine-hello-world",
        "args": {}
    },
    "alpine-http-server": {
        "path": "alpine-http-server/Dockerfile",
        "tag": "edvgui/alpine-http-server",
        "args": {}
    },
    "alpine-ping": {
        "path": "alpine-ping/Dockerfile",
        "tag": "edvgui/alpine-ping",
        "args": {}
    },
    "alpine-io-read": {
        "path": "alpine-io-read/Dockerfile",
        "tag": "edvgui/alpine-io-read-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "alpine-io-write": {
        "path": "alpine-io-write/Dockerfile",
        "tag": "edvgui/alpine-io-write-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "alpine-db-read": {
        "path": "alpine-db-read/Dockerfile",
        "tag": "edvgui/alpine-db-read-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "alpine-db-write": {
        "path": "alpine-db-write/Dockerfile",
        "tag": "edvgui/alpine-db-write-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "centos-hello-world": {
        "path": "centos-hello-world/Dockerfile",
        "tag": "edvgui/centos-hello-world",
        "args": {}
    },
    "centos-http-server": {
        "path": "centos-http-server/Dockerfile",
        "tag": "edvgui/centos-http-server",
        "args": {}
    },
    "centos-ping": {
        "path": "centos-ping/Dockerfile",
        "tag": "edvgui/centos-ping",
        "args": {}
    },
    "centos-io-read": {
        "path": "centos-io-read/Dockerfile",
        "tag": "edvgui/centos-io-read-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "centos-io-write": {
        "path": "centos-io-write/Dockerfile",
        "tag": "edvgui/centos-io-write-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "centos-db-read": {
        "path": "centos-db-read/Dockerfile",
        "tag": "edvgui/centos-db-read-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "centos-db-write": {
        "path": "centos-db-write/Dockerfile",
        "tag": "edvgui/centos-db-write-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    }
}

image_list = []


def compose_args(args):
    if len(args) == 0:
        yield ""
    else:
        for v in args[0]:
            for a in compose_args(args[1:]):
                yield "-%s%s" % (v, a)


for i in images:
    image = images[i]
    args = compose_args(list(image["args"].values()))
    for a in args:
        image_list.append("%s%s" % (i, a))


def usage():
    usage_msg = "Usage: python3 build.py [OPTIONS] IMAGE1 [IMAGE2 ..]\n" \
                "\n" \
                "Build the docker images\n\n" \
                "Options:\n" \
                "  -h, --help               Display this message\n" \
                "  -d, --directory path     Base directory for the Dockerfile (default: ./)\n" \
                "  -a, --all                Build all the images\n" \
                "  -m, --match string       Images that contains the string" \
                "\n" \
                "Images:\n  %s" % "\n  ".join(image_list)

    print(usage_msg)


def build(name, directory):
    image = None
    for i in images.keys():
        if i in name:
            image = images[i]
            name = "".join(name.split(i))
            break
    if image is None:
        print("Error identifying image from %s" % name)
        return

    parts = name.split("-")[1:]
    args = image["args"]
    if len(parts) != len(args.keys()):
        print("Error identifying args from %s" % name)
        return

    build_args = []

    for i in range(0, len(args)):
        if parts[i] not in list(args.values())[i]:
            print("Error finding args %s in %s" % (parts[i], list(args.values())[i]))
            return
        else:
            build_args.append("--build-arg")
            build_args.append("%s=%s" % (list(args.keys())[i], parts[i]))

    tag = image["tag"] % ("-".join(parts)) if len(build_args) > 0 else image["tag"]

    command = ["docker", "build", "-t", tag]
    command.extend(build_args)
    command.extend(["-f", os.path.join(directory, image["path"]), os.path.join(directory, "../")])
    print("INFO: %s: Building" % tag)
    output = subprocess.run(args=command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode != 0:
        print("Error building container: %s" % output.stderr.decode('utf-8'))
        return


def main(argv):
    directory = "/".join(argv[0].split("/")[0:-1])
    all_images = False
    match = []

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
        for i in image_list:
            build(i, directory)
        sys.exit(0)

    for m in match:
        for i in image_list:
            if m in i:
                build(i, directory)

    for a in args:
        if a not in image_list:
            print("Can not find %s in available images" % a)
        else:
            build(a, directory)


if __name__ == "__main__":
    main(sys.argv)
