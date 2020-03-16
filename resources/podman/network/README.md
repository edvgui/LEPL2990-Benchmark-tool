# Ping
Create a container that performs a few ping requests and prints the final result.

#### Build
We export our container from docker.  The container we export needs to be previously build with docker.  Build commands
can be found [here](../../docker/alpine/network/README.md).
```shell script
podman pull docker-daemon:alpine-network:latest
```

#### Launch
```shell script
docker run --rm alpine-network
```