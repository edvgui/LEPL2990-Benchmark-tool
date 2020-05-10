# Write on sqlite database
Create a container that contains a big database and performs a large amount of write operations on it.

#### Build
```shell script
# From within this directory
docker build -t alpine-db-write -f Dockerfile ../../../

# From anywhere else
docker build -t alpine-db-write -f path/to/mondial-write/Dockerfile path/to/mondial-write/../../..
```

#### Launch
```shell script
docker run --rm alpine-db-write
```