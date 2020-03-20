# Read on sqlite database
Create a container that contains a big database and performs a large amount of read operations on it.

#### Build
We export our container from docker.  The container we export needs to be previously build with docker.  Build commands
can be found [here](../../../docker/alpine/mondial-read/README.md).
```shell script
./../../commands/build alpine-mondial-read
```

#### Launch
```shell script
# Creating the container
export container=$(./../../commands/create alpine-mondial-read)

# Launching the container
runc run -b ../../pool/${container} ${container}

# Cleaning the container
./../../commands/clean ${container}
```