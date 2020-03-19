# Hello world
Create a container that prints a simple Hello World message in the console then quit.

#### Build
We export our container from docker.  The container we export needs to be previously build with docker.  Build commands
can be found [here](../../../docker/alpine/hello-world/README.md).
```shell script
./../../commands/build alpine-hello-world
```

#### Launch
```shell script
# Creating the container
export container=$(./../../commands/create alpine-hello-world)

# Launching the container
runc run -b ../../pool/${container} ${container}

# Cleaning the container
./../../commands/clean ${container}
```