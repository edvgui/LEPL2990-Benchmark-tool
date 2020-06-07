# Contingious

This is not another general purpose container manager, not yet at least.  This is a concept solution, that just fit the 
needs of INGInious in terms of container management.  It relies on the idea that we can predict for each container which
part of its file system will be modified.  We use this knowledge to make split the filesystem in two entities:
 - The first part, editable, copied at the creation of each container
 - The second part, read-only, bind mounted into the first one
 
This allows us to have nearly native writing performances, while avoiding copying file we don't need to.

On top of that, Contingious directly interact with a container runtime, `crun`.

### Reproducing the behaviour of Contingious
#### Importing an image

To create a container, we first need an image.  A bunch of preconfigured images can be retrieved using 
[import.py](import.py):
```console
$ ./import.py --images-path /tmp/my-images alpine-hello-world
INFO: Pulling from docker edvgui/alpine-hello-world
Getting image source signatures
Copying blob cbdbe7a5bc2a done  
Copying config 8f567b66a9 done  
Writing manifest to image destination
Storing signatures
INFO: Retrieving image info
INFO: Mounting container alpine-hello-world-working-container
INFO: Already an image with this name, removing...
INFO: Copying editable rootfs
INFO: Copying read-only rootfs
INFO: Saving command
INFO: Unmounting container filesystem
INFO: Unmounting container alpine-hello-world-working-container
INFO: Removing temporary container
INFO: Cleaning container alpine-hello-world-working-container
INFO: Removing temporary container image
INFO: Cleaning image edvgui/alpine-hello-world
```
> Note that this tool relies on [Buildah](https://github.com/containers/buildah), which has to be already installed on 
> the system

#### Creating a container
We can first copy our writable filesystem in a new directory, and generate a configuration file for our container
```console
~$ mkdir -p /tmp/my-containers/test
~$ cp -r /tmp/my-images/edvgui/alpine-hello-world/rootfs /tmp/my-containers/test/rootfs
~$ cd /tmp/my-containers/test
/tmp/my-containers/test$ crun spec --rootless
```
This will generate a file, `config.json`, we will need to modify it a little bit:

<details>

<summary>Click here to expand the list of modifications to apply</summary>

 -  We can change `process.args` to match the command we want to execute:
    ```json
    {
      "process": {
        "terminal": false,
        "args": [
          "/bin/echo",
          "Hello",
          "World"
        ] 
      }
    }
    ```
 -  We have to allow to mark the filesystem as editable:
    ```json
    {
      "root": {
         "path": "/tmp/my-containers/test/rootfs",
         "readonly": false
      }
    }
    ```
 -  We have to mount the read-only part of our file-system:
    ```json
    {
      "mounts": [
        {
          "destination": "/mnt",
          "type": "bind",
          "source": "/mnt/my-images/edvgui/alpine-hello-world/ro-rootfs",
          "options": [
            "bind",
            "private",
            "ro"
          ]
        },
        ...
      ]
    }
    ```
 -  We can add resource limitation to the container too:
    ```json
    {
      "linux": {
        "resources": {
          "memory": {
                "limit": 1073741824,
                "disableOOMKiller": false
            },
            "cpu": {
                "quota": 100000,
                "period": 100000
            },
            "pids": {
                "limit": 4096
            }
        },
        "cgroupsPath": "user.slice:contingious:test"
      }
    }
    ```
 -  Finally, we have to remove the user namespace from the list of namespaces to create, as we will deal with this later:
    ```json
    {
      "linux": {
        "namespaces": [
                {
                        "type": "pid"
                },
                {
                        "type": "network"
                },
                {
                        "type": "ipc"
                },
                {
                        "type": "uts"
                },
                {
                        "type": "mount"
                }
        ]
      }
    }
    ```

</details>

Once the configuration file is ready, we can unshare the user and mount namespaces with rootlesskit.  We can see that we
appear as root in the namespace, but we aren't for real, our uid as simply be mapped to root inside of the user 
namespace.  We can then launch our container.
```console
/tmp/my-containers/test$ rootlesskit bash
/tmp/my-containers/test# whoami
root
/tmp/my-containers/test# crun --systemd-cgroup run test
Hello World
```

#### Executing a command in an already running container
If we want to add a process in a running container, we don't need to recreate the user and mount namespace with 
rootlesskit, we simply need to re-enter those namespaces, and use `crun` to execute the command we want.

If we modify the configuration from the previous example:
```json
{
  "process": {
    "terminal": true,
    "args": [
      "sh"
    ] 
  }
}
```

We can in first terminal, run the container:
```console
/tmp/my-containers/test$ rootlesskit bash
/tmp/my-containers/test# echo $$ > /tmp/pid
/tmp/my-containers/test# crun --systemd-cgroup run test
/# 
```

And in a second terminal, add a command to the already running container:
```console
/tmp/my-containers/test$ systemd-run --user --scope --quiet nsenter --user --mount -t $(cat /tmp/pid) bash
/# 
/# crun --systemd-cgroup exec -t test echo Hello World
Hello World
```
