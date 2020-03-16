# Write on sqlite database
Create a container that contains a big database and performs a large amount of write operations on it.

#### Build
```shell script
# From within this directory
docker build -t centos-mondial-write -f Dockerfile ../../../

# From anywhere else
docker build -t centos-mondial-write -f path/to/mondial-read/Dockerfile path/to/mondial-read/../../..
```

#### Launch
```shell script
docker run --rm centos mondial-write
```