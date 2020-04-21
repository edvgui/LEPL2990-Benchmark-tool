import array
import json
import os
import shutil
import socket
import subprocess
import random
from subprocess import Popen, PIPE
from enum import Enum


class State(Enum):

    NEW = "new"
    READY = "ready"
    CREATED = "created"
    RUNNING = "running"
    STOPPED = "stopped"
    DONE = "done"

    def __str__(self):
        return self.value


class ContainerException(Exception):

    def __init__(self, command, message):
        self.command = command
        self.message = message

    def __str__(self):
        return "ContainerException: while executing {0}\n{1}".format(self.command, self.message)


class ContainerLifeCycleException(ContainerException):

    def __init__(self, expected, actual, command, message):
        super().__init__(command, message)
        self.expected = expected
        self.actual = actual

    def __str__(self):
        return "ContainerLifeCycleException: while executing {0}, expecting {1}, got {2}\n{3}".format(
            self.command, self.expected, self.actual, self.message)


class ContainerRuntimeException(ContainerException):

    def __init__(self, runtime, command, message):
        super().__init__(command, message)
        self.runtime = runtime

    def __str__(self):
        return "ContainerRuntimeException [{0}]: while executing {1} \n{2}".format(self.runtime, self.command, self.message)


class Container:

    def __init__(self, socket_folder, pool_folder):
        self.__id = generate_safe_id(socket_folder, pool_folder)
        self.path = os.path.join(pool_folder, self.__id)
        self.image = None
        self.name = self.__id
        self.network = False
        self.port = None
        self.auto_remove = False
        self.tty = None
        self.runtime = None
        self.cmd = None
        self.state = State.NEW
        self.shell = None

    def get_id(self):
        return self.__id

    def __setup(self, image, runtime, name=None, network=False, port=None, auto_remove=False, terminal=False, cmd=None):
        if self.state != State.NEW:
            raise ContainerLifeCycleException(State.NEW, self.state, "setup", "Container has already been setup")

        self.image = image
        self.network = network
        self.port = port
        self.auto_remove = auto_remove
        self.runtime = runtime

        if name is not None:
            self.name = name

        if cmd is not None:
            self.cmd = cmd
        else:
            self.cmd = load_cmd(self.image)

        create_rootfs(self.image, self.path)
        mount_ro_rootfs(self.image, self.path)

        state_dir = os.path.join(self.path, 'state-dir')
        shell_startup = []
        if network:
            shell_startup.extend(["/usr/bin/rootlesskit", "--net=slirp4netns", "--disable-host-loopback", "--copy-up=/etc"])
            if port:
                shell_startup.extend(["--state-dir", state_dir, "--port-driver=builtin"])

        shell_startup.extend(["/usr/bin/env", "bash"])
        self.shell = Popen(shell_startup, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)

        if network and port:
            setup_port = "/usr/bin/rootlessctl --socket={0}/api.sock add-ports {1} > /dev/null".format(state_dir, self.port)
            return_code, out = shell_command(self.shell, setup_port, "ESC-" + self.get_id() + "-CSE")
            if return_code != "0":
                raise ContainerRuntimeException(self.runtime, setup_port,
                                                "Error while creating port: %s" % out)

        generate_spec = "{0} --root {1} spec --rootless -b {2}".format(self.runtime["path"], self.runtime["root"], self.path)
        return_code, out = shell_command(self.shell, generate_spec, "ESC-" + self.get_id() + "-CSE")
        if return_code != "0":
            raise ContainerRuntimeException(self.runtime, generate_spec, "Error while generating spec: %s" % out)
        setup_config(self.path, self.cmd, network, terminal)

        self.state = State.READY

    def create(self, image, runtime, name=None, network=False, port=None, auto_remove=False, terminal=False, cmd=None):
        self.__setup(image, runtime, name, network, port, auto_remove, terminal, cmd)

        if self.state != State.READY:
            raise ContainerLifeCycleException(State.READY, self.state, "create", "Container has to be ready to be "
                                                                                 "created")

        if terminal:
            console_socket = os.path.join('/', 'tmp', self.get_id() + "-tty.sock")
            sock = create_console_socket(console_socket)
            create_container = "{0} --root {1} create -b {2} --console-socket {3} {4}".format(
                self.runtime["path"], self.runtime["root"], self.path, console_socket, self.get_id())
            return_code, out = shell_command(self.shell, create_container, "ESC-" + self.get_id() + "-CSE")
            if return_code != "0":
                raise ContainerRuntimeException(self.runtime, create_container,
                                                "Error while creating container: %s" % out)
            self.tty = retrieve_console_fd(sock)
        else:
            create_container = "{0} --root {1} create -b {2} {3}".format(
                self.runtime["path"], self.runtime["root"], self.path, self.get_id())
            return_code, out = shell_command(self.shell, create_container, "ESC-" + self.get_id() + "-CSE")
            if return_code != "0":
                raise ContainerRuntimeException(self.runtime, create_container,
                                                "Error while creating container: %s" % out)

        self.state = State.CREATED
        return self.get_id()

    def start(self, attach=False):
        if self.state != State.CREATED:
            raise ContainerLifeCycleException(State.CREATED, self.state, "start", "Container has to be created to be "
                                                                                  "started")

        start_container = "{0} --root {1} start {2}".format(self.runtime["path"], self.runtime["root"], self.get_id())
        return_code, out = shell_command(self.shell, start_container, "ESC-" + self.get_id() + "-CSE")
        if return_code != "0":
            raise ContainerRuntimeException(self.runtime, start_container, "Error while starting container: %s" % out)

        self.state = State.RUNNING
        return self.get_id()

    def exec(self, cmd, detach=False, terminal=False):
        if self.state != State.RUNNING:
            raise ContainerLifeCycleException(State.RUNNING, self.state, "exec", "You can only execute a command in a "
                                                                                 "running container")

    def kill(self):
        if self.state != State.RUNNING:
            raise ContainerLifeCycleException(State.RUNNING, self.state, "kill", "You can only kill a container that is"
                                                                                 " running")

        kill_container = "{0} --root {1} kill -a {2}".format(self.runtime["path"], self.runtime["root"], self.get_id())
        return_code, out = shell_command(self.shell, kill_container, "ESC-" + self.get_id() + "-CSE")
        if return_code != "0":
            raise ContainerRuntimeException(self.runtime, kill_container, "Error while killing container: %s" % out)

        self.state = State.STOPPED

        if self.auto_remove:
            return self.rm()
        else:
            return self.get_id()

    def rm(self):
        if self.state != State.STOPPED:
            raise ContainerLifeCycleException(State.STOPPED, self.state, "rm", "You can only delete a stopped container")

        delete_container = "{0} --root {1} delete {2}".format(self.runtime["path"], self.runtime["root"], self.get_id())
        return_code, out = shell_command(self.shell, delete_container, "ESC-" + self.get_id() + "-CSE")
        if return_code != "0":
            raise ContainerRuntimeException(self.runtime, delete_container, "Error while deleting container: %s" % out)

        self.shell.stdin.write(b'exit\n')
        self.shell.stdin.flush()
        self.shell.terminate()
        del self.shell

        unmount_ro_rootfs(self.path)
        delete_rootfs(self.path)

        self.state = State.DONE

        return self.get_id()

    def run(self, image, runtime, name=None, detach=False, network=False, port=None, auto_remove=False, terminal=False, cmd=None):
        self.__setup(image, runtime, name, network, port, auto_remove, terminal, cmd)

        if self.state != State.READY:
            raise ContainerLifeCycleException(State.READY, self.state, "create", "Container has to be ready to be run")

        self.state = State.RUNNING
        return self.get_id()


def shell_command(shell, command, escape):
    command += "; printf \"" + escape + "\\n$?\\n\"\n"
    shell.stdin.write(bytes(command, 'utf-8'))
    shell.stdin.flush()
    out = ""
    line = shell.stdout.readline().decode('utf-8').strip()
    while line != escape:
        out += line + "\n"
        line = shell.stdout.readline().decode('utf-8').strip()
    return_code = shell.stdout.readline().decode('utf-8').strip()
    return return_code, out


def generate_safe_id(socket_folder, pool_folder):
    hash_b = random.getrandbits(128)
    _id = "%032x" % hash_b
    while os.path.isdir(os.path.join(socket_folder, _id)) or os.path.isdir(os.path.join(pool_folder, _id)):
        hash_b = random.getrandbits(128)
        _id = "%032x" % hash_b
    return _id


def load_cmd(image_path):
    cmd = os.path.join(image_path, "CMD")
    with open(cmd, "r") as f:
        c = f.readline().strip()
        f.close()
    return c.split(" ")


def create_rootfs(image_path, container_path):
    src = os.path.join(image_path, "rootfs")
    dst = os.path.join(container_path, "rootfs")
    os.mkdir(container_path)
    shutil.copytree(src, dst, symlinks=True)


def delete_rootfs(container_path):
    shutil.rmtree(container_path)


def mount_ro_rootfs(image_path, container_path):
    src = os.path.join(image_path, 'ro-rootfs')
    dst = os.path.join(container_path, 'rootfs', 'mnt')
    args = ["bindfs", "-p", "555", "--no-allow-other", src, dst]
    output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode != 0:
        raise ContainerException(args, "ERROR: Couldn't bind mount read-only filesystem: %s" % output.stderr.decode('utf-8'))


def unmount_ro_rootfs(container_path):
    args = ["fusermount", "-u", os.path.join(container_path, 'rootfs', 'mnt')]
    output = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if output.returncode != 0:
        raise ContainerException(args, "ERROR: Couldn't unmount read-only filesystem: %s" % output.stderr.decode('utf-8'))


def setup_config(container_path, cmd, network, terminal):
    config_path = os.path.join(container_path, 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
        f.close()

    config["root"]["readonly"] = False
    config["process"]["terminal"] = terminal
    config["process"]["args"] = cmd

    if network:
        capabilities = config["process"]["capabilities"]
        for c in capabilities:
            capabilities[c].append("CAP_NET_RAW")
        config["linux"]["uidMappings"] = [{"containerID": 0, "hostID": 1, "size": 1}]
        config["linux"]["gidMappings"] = [{"containerID": 0, "hostID": 1, "size": 1}]
        config["linux"]["namespaces"] = [{"type": "pid"}, {"type": "ipc"}, {"type": "uts"}, {"type": "mount"}]
    else:
        config["linux"]["namespaces"] = [{"type": "pid"}, {"type": "network"}, {"type": "ipc"}, {"type": "uts"},
                                         {"type": "mount"}, {"type": "user"}]

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
        f.close()


def create_console_socket(console_socket):
    sock = socket.socket(socket.AF_UNIX)
    sock.bind(console_socket)
    sock.listen()
    return sock


def retrieve_console_fd(sock):
    fds = array.array('i')
    conn, _ = sock.accept()
    sock.close()
    msg, ancdata, msg_flags, _addr = conn.recvmsg(16, socket.CMSG_SPACE(fds.itemsize), socket.MSG_CMSG_CLOEXEC, )
    cmsg_level, cmsg_type, cmsg_data = ancdata[0]
    assert cmsg_level == socket.SOL_SOCKET, cmsg_level
    assert cmsg_type == socket.SCM_RIGHTS, cmsg_type
    fds.frombytes(cmsg_data)
    return list(fds)[0]
