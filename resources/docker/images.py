#!/usr/bin/env python3

__images = {
    "alpine-hello-world": {
        "src": "alpine-hello-world/Dockerfile",
        "tag": "edvgui/alpine-hello-world",
        "args": {}
    },
    "alpine-http-server": {
        "src": "alpine-http-server/Dockerfile",
        "tag": "edvgui/alpine-http-server",
        "args": {}
    },
    "alpine-ping": {
        "src": "alpine-ping/Dockerfile",
        "tag": "edvgui/alpine-ping",
        "args": {}
    },
    "alpine-io-read": {
        "src": "alpine-io-read/Dockerfile",
        "tag": "edvgui/alpine-io-read-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "alpine-io-write": {
        "src": "alpine-io-write/Dockerfile",
        "tag": "edvgui/alpine-io-write-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "alpine-db-read": {
        "src": "alpine-db-read/Dockerfile",
        "tag": "edvgui/alpine-db-read-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "alpine-db-write": {
        "src": "alpine-db-write/Dockerfile",
        "tag": "edvgui/alpine-db-write-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "centos-hello-world": {
        "src": "centos-hello-world/Dockerfile",
        "tag": "edvgui/centos-hello-world",
        "args": {}
    },
    "centos-http-server": {
        "src": "centos-http-server/Dockerfile",
        "tag": "edvgui/centos-http-server",
        "args": {}
    },
    "centos-ping": {
        "src": "centos-ping/Dockerfile",
        "tag": "edvgui/centos-ping",
        "args": {}
    },
    "centos-io-read": {
        "src": "centos-io-read/Dockerfile",
        "tag": "edvgui/centos-io-read-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "centos-io-write": {
        "src": "centos-io-write/Dockerfile",
        "tag": "edvgui/centos-io-write-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "centos-db-read": {
        "src": "centos-db-read/Dockerfile",
        "tag": "edvgui/centos-db-read-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "centos-db-write": {
        "src": "centos-db-write/Dockerfile",
        "tag": "edvgui/centos-db-write-%s",
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    }
}
__image_list = []


def get_images():
    if len(__image_list) == 0:
        def compose_args(args):
            if len(args) == 0:
                yield ""
            else:
                for v in args[0]:
                    for a in compose_args(args[1:]):
                        yield "-%s%s" % (v, a)

        for i in __images:
            image = __images[i]
            args = compose_args(list(image["args"].values()))
            for a in args:
                __image_list.append("%s%s" % (i, a))

    return __image_list


def get_image(name):
    image = None
    for i in __images.keys():
        if i in name:
            image = __images[i]
            name = "".join(name.split(i))
            break
    if image is None:
        print("Error identifying image from %s" % name)
        return None

    parts = name.split("-")[1:]
    args = image["args"]
    if len(parts) != len(args.keys()):
        print("Error identifying args from %s" % name)
        return

    build_args = {}

    for arg in args:
        part = parts.pop()
        possibilities = args[arg]
        if part in possibilities:
            build_args[arg] = part

    parts = list(build_args.values())

    tag = image["tag"] % ("-".join(parts)) if len(parts) > 0 else image["tag"]

    return image["src"], tag, build_args
