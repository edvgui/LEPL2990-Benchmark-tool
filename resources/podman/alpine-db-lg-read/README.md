# Read on sqlite database
Create a container that contains a big database and performs a large amount of read operations on it.

#### Build
We export our container from docker.  The container we export needs to be previously build with docker.  Build commands
can be found [here](../../docker/alpine/mondial-read/README.md).
```shell script
podman pull docker-daemon:alpine-db-read:latest
```

#### Launch
```shell script
docker run --rm alpine-db-read
```