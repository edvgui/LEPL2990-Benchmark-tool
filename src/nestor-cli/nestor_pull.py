#!/usr/bin/env python3
import shutil
import sys
import docker
import getopt
import tarfile
import os


from nestor_config import load as get_config


def usage():
    usage_msg = "Usage: nestor pull [OPTIONS] IMAGE\n" \
        "\n" \
        "Build a new container image from its docker equivalent\n\n" \
        "Options:\n" \
        "  -t, --tag string        The tag to give to the image\n" \
        "      --read-only string  The root folders to set as read-only\n"
    print(usage_msg)


def check_docker(image):
    client = docker.from_env()

    found = False
    for docker_image in client.images.list():
        if image in docker_image.tags:
            found = True

    if not found:
        raise Exception("Error: docker image not found")


def export_docker(image, dst):
    client = docker.from_env()
    with open(dst, 'wb+', buffering=0) as f:
        exp = client.images.get(image).save()
        for b in exp:
            f.write(b)
        f.close()
    return client.api.inspect_image(image)["Config"]["Cmd"][2]


def extract_rootfs(src, rootfs):
    with open(src, 'rb') as f:
        with tarfile.open(mode="r|", fileobj=f) as tar:
            for tarinfo in tar:
                tar.extract(tarinfo, rootfs)
            tar.close()
        f.close()


def pull(image, images_path, tag, ro_s):
    image_dir = os.path.join(images_path, tag)
    if os.path.exists(image_dir):
        print("ERROR: There is already an image with this tag: %s" % tag)
        sys.exit(1)

    rootfs = os.path.join(image_dir, 'rootfs')
    ro_rootfs = os.path.join(image_dir, 'ro-rootfs')

    r, w = os.pipe()
    process_id = os.fork()
    if process_id:
        cmd = export_docker(image, w)
    else:
        extract_rootfs(r, rootfs)
        sys.exit(0)

    try:
        # Create read-only rootfs
        os.mkdir(ro_rootfs)
    except OSError as e:
        print("ERROR: %s" % e.strerror)

    # Move and symlink read-only folders
    for ro in ro_s:
        try:
            shutil.move(os.path.join(rootfs, ro), os.path.join(ro_rootfs, ro))
            os.symlink(os.path.join('mnt', ro), os.path.join(rootfs, ro))
        except shutil.Error as e:
            print("ERROR: %s" % e.strerror)

    # Saving starting command in file
    with open(os.path.join(image_dir, "CMD"), "w+") as f:
        f.write(cmd)
        f.close()


def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "t:", ["tag=", "read-only="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(args) != 1:
        usage()
        exit(1)

    image = args[0]
    tag = image.split(":")[0]
    check_docker(image)
    ro_s = []

    for opt, arg in opts:
        if opt in ('-t', '--tag'):
            tag = arg
        if opt == '--read-only':
            ro_s = arg.split(",")

    config = get_config()
    try:
        images_storage = config["storage"]["images"]
    except KeyError:
        print("ERROR: Bad configuration file, missing storage.images")
        sys.exit(1)

    pull(image, images_storage, tag, ro_s)
