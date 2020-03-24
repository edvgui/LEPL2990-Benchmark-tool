# Http server
Create a container that prints a simple Hello World message in the console then quit.

#### Build
We export our container from docker.  The container we export needs to be previously build with docker.  Build commands
can be found [here](../../docker/alpine/http-server/README.md).
```shell script
podman pull docker-daemon:alpine-http-server:latest
```

#### Launch
```shell script
podman run --rm -d -p 127.0.0.1:3000:80 alpine-http-server 
```