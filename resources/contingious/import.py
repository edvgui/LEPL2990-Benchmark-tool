#!/usr/bin/env python3

import getopt
import os
import shutil
import subprocess
import sys

from images import get_image, get_images


def usage():
    usage_msg = "Usage: python3 build.py [OPTIONS] IMAGE1 [IMAGE2 ..]\n" \
                "\n" \
                "Build the lxc images\n\n" \
                "Options:\n" \
                "  -h, --help               Display this message\n" \
                "      --images-path path   Base directory where to save images\n" \
                "  -a, --all                Build all the images\n" \
                "  -m, --match string       Images that contains the string" \
                "\n" \
                "Images:\n  %s" % "\n  ".join(get_images())

    print(usage_msg)


def pull(tag):
    command = "buildah --storage-driver vfs --root /tmp/contingious-build --runroot /tmp/contingious-build from " \
              "--pull-always %s:latest" % tag
    print("INFO: Pulling from docker %s" % tag)
    output = subprocess.run(args=command.split(" "), stdout=subprocess.PIPE)
    if output.returncode != 0:
        print("Error pulling %s" % tag)
        return None
    return output.stdout.decode('utf-8').strip()


def mount(container):
    command = "buildah --storage-driver vfs --root /tmp/contingious-build --runroot /tmp/contingious-build unshare " \
              "buildah --storage-driver vfs --root /tmp/contingious-build --runroot /tmp/contingious-build mount %s" \
              % container
    print("INFO: Mounting container %s" % container)
    output = subprocess.run(args=command.split(" "), stdout=subprocess.PIPE)
    if output.returncode != 0:
        print("Error mounting %s" % container)
        return None
    return output.stdout.decode('utf-8').strip()


def umount(container):
    command = "buildah --storage-driver vfs --root /tmp/contingious-build --runroot /tmp/contingious-build unshare " \
              "buildah --storage-driver vfs --root /tmp/contingious-build --runroot /tmp/contingious-build umount %s" \
              % container
    print("INFO: Unmounting container %s" % container)
    output = subprocess.run(args=command.split(" "), stdout=subprocess.PIPE)
    if output.returncode != 0:
        print("Error unmounting %s" % container)
        return False
    return True


def rm(container):
    command = "buildah --storage-driver vfs --root /tmp/contingious-build --runroot /tmp/contingious-build rm %s" \
              % container
    print("INFO: Cleaning container %s" % container)
    output = subprocess.run(args=command.split(" "), stdout=subprocess.PIPE)
    if output.returncode != 0:
        print("Error cleaning %s" % container)
        return None
    return output.stdout.decode('utf-8')


def build(name, directory):
    tag, ro, wr = get_image(name)

    # Pull image and mount its fs with buildah
    container = pull(tag)
    if container is None:
        return
    mount_path = mount(container)
    if mount_path is None:
        rm(container)
        return

    image_dir = os.path.join(directory, tag)

    if os.path.exists(image_dir):
        print("INFO: Already an image with this name, removing...")
        shutil.rmtree(image_dir, ignore_errors=True)

    print("INFO: Copying editable rootfs")
    rootfs = os.path.join(image_dir, 'rootfs')
    os.makedirs(rootfs)
    for d in wr:
        src = os.path.join(mount_path, d)
        dst = os.path.join(rootfs, d)
        # For some reason `shutil.copytree` hangs on some directories
        command = "cp -r %s %s" % (src, dst)
        output = subprocess.run(args=command.split(" "), stdout=subprocess.PIPE)
        if output.returncode != 0:
            print("Error copying %s to %s" % (src, dst))
            print("INFO: Unmounting container filesystem")
            umount(container)

            print("INFO: Removing temporary container")
            rm(container)
            return

    print("INFO: Copying read-only rootfs")
    ro_rootfs = os.path.join(image_dir, 'ro-rootfs')
    os.makedirs(ro_rootfs)
    for d in ro:
        src = os.path.join(mount_path, d)
        dst = os.path.join(ro_rootfs, d)
        # For some reason `shutil.copytree` hangs on some directories
        command = "cp -r %s %s" % (src, dst)
        output = subprocess.run(args=command.split(" "), stdout=subprocess.PIPE)
        if output.returncode != 0:
            print("Error copying %s to %s" % (src, dst))
            print("INFO: Unmounting container filesystem")
            umount(container)

            print("INFO: Removing temporary container")
            rm(container)
            return
        os.symlink(os.path.join('mnt', d), os.path.join(rootfs, d))

    print("INFO: Unmounting container filesystem")
    umount(container)

    print("INFO: Removing temporary container")
    rm(container)


def main(argv):
    images_path = os.path.join(os.path.expanduser("~"), '.local/share/contingious/storage/images')
    all_images = False
    match = []

    if len(argv) == 1:
        usage()
        sys.exit(0)

    try:
        opts, args = getopt.getopt(argv[1:], "hd:am:", ["help", "images-path=", "all", "match="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "--images-path":
            images_path = arg
        elif opt == "--all":
            all_images = True
        elif opt in ("-m", "--match"):
            match.append(arg)

    if all_images:
        for i in get_images():
            build(i, images_path)
        sys.exit(0)

    for m in match:
        for i in get_images():
            if m in i:
                build(i, images_path)

    for a in args:
        if a not in get_images():
            print("Can not find %s in available images" % a)
        else:
            build(a, images_path)


if __name__ == "__main__":
    main(sys.argv)
