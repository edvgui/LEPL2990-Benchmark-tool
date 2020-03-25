# Http server
Create a container that launches a lightweight http server.

#### Build
We export our container from docker.  The container we export needs to be previously build with docker.  Build commands
can be found [here](../../docker/alpine-hello-world/README.md).
```shell script
./../build alpine-hello-world
```

#### Launch
```shell script
# Creating the container
export container=$(./../create alpine-http-server)

# Launching the container
./../run --detach --port 127.0.0.1:3000:80/tcp ${container}

# Stop the container
./../stop ${container}

# Cleaning the container
./../clean ${container}
```