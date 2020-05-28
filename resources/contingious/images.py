#!/usr/bin/env python3

__images = {
    "alpine-hello-world": {
        "tag": "edvgui/alpine-hello-world",
        "ro": ["bin", "dev", "etc", "lib", "run", "sbin", "usr", "var"],
        "wr": ["home", "media", "mnt", "opt", "root", "srv", "sys", "tmp"],
        "args": {}
    },
    "alpine-http-server": {
        "tag": "edvgui/alpine-http-server",
        "ro": ["bin", "dev", "etc", "lib", "sbin", "usr"],
        "wr": ["home", "media", "mnt", "opt", "root", "run", "srv", "sys", "tmp", "var"],
        "args": {}
    },
    "alpine-ping": {
        "tag": "edvgui/alpine-ping",
        "ro": ["bin", "dev", "etc", "lib", "run", "sbin", "usr", "var"],
        "wr": ["home", "media", "mnt", "opt", "root", "srv", "sys", "tmp"],
        "args": {}
    },
    "alpine-io-read": {
        "tag": "edvgui/alpine-io-read-%s",
        "ro": ["bin", "dev", "etc", "lib", "run", "sbin", "usr", "var"],
        "wr": ["home", "media", "mnt", "opt", "root", "srv", "sys", "tmp"],
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "alpine-io-write": {
        "tag": "edvgui/alpine-io-write-%s",
        "ro": ["bin", "dev", "etc", "lib", "run", "sbin", "usr", "var"],
        "wr": ["home", "media", "mnt", "opt", "root", "srv", "sys", "tmp"],
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "alpine-db-read": {
        "tag": "edvgui/alpine-db-read-%s",
        "ro": ["bin", "dev", "etc", "lib", "run", "sbin", "usr", "var"],
        "wr": ["home", "media", "mnt", "opt", "root", "srv", "sys", "tmp"],
        "args": {
            "size": ["xs", "sm", "md", "lg", "xl"]
        }
    },
    "alpine-db-write": {
        "tag": "edvgui/alpine-db-write-%s",
        "ro": ["bin", "dev", "etc", "lib", "run", "sbin", "usr", "var"],
        "wr": ["home", "media", "mnt", "opt", "root", "srv", "sys", "tmp"],
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
        else:
            print("Error matching args, %s in not in %s" % (part, possibilities))
            return

    parts = list(build_args.values())

    tag = image["tag"] % ("-".join(parts)) if len(parts) > 0 else image["tag"]

    return tag, image["ro"], image["wr"]
