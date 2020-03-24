# Hello world
Create a Podman container that prints a simple Hello World message in the console then quit.

#### Build
We export our container from docker.  The container we export needs to be previously build with docker.  Build commands
can be found [here](../../docker/alpine/hello-world/README.md).
```shell script
podman pull docker-daemon:alpine-hello-world:latest
```

#### Launch
```shell script
podman run --rm alpine-hello-world
```