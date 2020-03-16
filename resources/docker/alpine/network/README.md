# Ping
Create a container that performs a few ping requests and prints the final result.

#### Build
```shell script
# From within this directory
docker build -t alpine-network -f Dockerfile ../../../

# From anywhere else
docker build -t alpine-network -f path/to/network/Dockerfile path/to/network/../../..
```

#### Launch
```shell script
docker run --rm alpine-network
```