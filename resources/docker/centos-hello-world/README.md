# Hello world
Create a Docker container that prints a simple Hello World message in the console then quit.

#### Build
```shell script
# From within this directory
docker build -t centos-hello-world .
```

#### Launch
```shell script
docker run --rm centos-hello-world
```