# Ping
Create a container that performs a few ping requests and prints the final result.

#### Build
We export our container from docker.  The container we export needs to be previously build with docker.  Build commands
can be found [here](../../docker/alpine-network/README.md).
```shell script
./../build alpine-hello-world
```

#### Launch
```shell script
# Creating the container
export container=$(./../create alpine-hello-world)

# Launching the container
./../run ${container}

# Cleaning the container
./../clean ${container}
```